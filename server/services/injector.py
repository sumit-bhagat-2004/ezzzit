import json
from pathlib import Path

# Path to the tracer template sitting next to this services/ package
_TRACER_PATH = Path(__file__).parent.parent / "tracer" / "python_tracer_template.py"

MAX_CODE_LINES = 300  # hard guardrail for hackathon stability


def _indent(code: str, spaces: int = 4) -> str:
    """Indent every line of *code* by *spaces* spaces."""
    pad = " " * spaces
    return "\n".join(pad + line for line in code.splitlines())


def inject_python_tracer(user_code: str) -> str:
    """
    Wraps *user_code* with the sys.settrace harness so that every line
    executed is recorded into TRACE_DATA.

    Strategy
    --------
    1. Read the tracer template (defines globals + tracer fn, no settrace call).
    2. Compute exactly which absolute line numbers user code occupies in the
       assembled script by measuring the prefix with placeholder values
       (same line count, different chars – splitlines is length-safe).
    3. Inject USER_CODE_START / USER_CODE_END, THEN activate sys.settrace and
       set f_trace on the current frame so module-level code is also traced.

    The final stdout will look like:
        <program output>
        __TRACE_START__
        [{ ...trace steps... }]
        __TRACE_END__
    """
    if len(user_code.splitlines()) > MAX_CODE_LINES:
        raise ValueError(
            f"Code exceeds the {MAX_CODE_LINES}-line limit "
            f"({len(user_code.splitlines())} lines submitted)."
        )

    tracer_src = _TRACER_PATH.read_text(encoding="utf-8")

    # ── Step 1: measure prefix length with placeholder values ─────────────────
    # Using single-digit placeholders keeps the line count identical to the
    # real version (splitlines counts newlines, not character width).
    _prefix_probe = (
        tracer_src
        + "\n"
        + "USER_CODE_START = 0\n"
        + "USER_CODE_END = 0\n"
        + "\n"
        + "sys.settrace(tracer)\n"
        + "sys._getframe().f_trace = tracer\n"
        + "\n"
        + "# ─── User code ──────────────────────────────────────────────────────────────\n"
        + "try:\n"
    )
    user_code_start = len(_prefix_probe.splitlines()) + 1  # 1-based; user code is the NEXT line
    user_code_end = user_code_start + len(user_code.splitlines()) - 1

    # ── Step 2: build the real prefix with computed line numbers ──────────────
    prefix = (
        tracer_src
        + "\n"
        + f"USER_CODE_START = {user_code_start}\n"
        + f"USER_CODE_END = {user_code_end}\n"
        + "\n"
        + "sys.settrace(tracer)\n"
        + "sys._getframe().f_trace = tracer  # enables tracing for module-level code\n"
        + "\n"
        + "# ─── User code ──────────────────────────────────────────────────────────────\n"
        + "try:\n"
    )

    # ── Step 3: assemble full script ──────────────────────────────────────────
    injected = (
        prefix
        + _indent(user_code) + "\n"
        + "except Exception as _exc:\n"
        + "    import traceback as _tb\n"
        + '    print("__TRACE_EXCEPTION__")\n'
        + "    print(_tb.format_exc())\n"
        + "finally:\n"
        + "    # Capture final state before disabling tracer\n"
        + "    _final_frame = sys._getframe()\n"
        + "    if TRACE_DATA and USER_CODE_START <= USER_CODE_END:\n"
        + "        # Create a final snapshot with all variable states\n"
        + "        def _serialize_final(obj, depth=0, max_depth=3):\n"
        + "            if depth > max_depth:\n"
        + "                return '...'\n"
        + "            if obj is None or isinstance(obj, (int, float, str, bool)):\n"
        + "                return obj\n"
        + "            if isinstance(obj, set):\n"
        + "                return {'__type__': 'set', 'items': [_serialize_final(x, depth+1) for x in sorted(list(obj), key=str)]}\n"
        + "            if type(obj).__name__ == 'deque':\n"
        + "                return {'__type__': 'deque', 'items': [_serialize_final(x, depth+1) for x in list(obj)]}\n"
        + "            if isinstance(obj, (list, tuple)):\n"
        + "                return [_serialize_final(x, depth+1) for x in obj]\n"
        + "            if isinstance(obj, dict):\n"
        + "                return {k: _serialize_final(v, depth+1) for k, v in obj.items()}\n"
        + "            if hasattr(obj, '__dict__'):\n"
        + "                return {'__type__': type(obj).__name__, '__id__': str(id(obj)), **{k: _serialize_final(v, depth+1) for k, v in vars(obj).items() if not k.startswith('_')}}\n"
        + "            return repr(obj)\n"
        + "        \n"
        + "        _final_vars = {}\n"
        + "        _all_vars = {**_final_frame.f_globals, **_final_frame.f_locals}\n"
        + "        for _k, _v in _all_vars.items():\n"
        + "            if _k in _HARNESS_VARS or _k.startswith('__') or _k.startswith('_'):\n"
        + "                continue\n"
        + "            if callable(_v) and hasattr(_v, '__module__'):\n"
        + "                if _v.__module__ in ('builtins', 'sys', 'json'):\n"
        + "                    continue\n"
        + "            try:\n"
        + "                _final_vars[_k] = _serialize_final(_v)\n"
        + "            except Exception:\n"
        + "                _final_vars[_k] = repr(_v)\n"
        + "        \n"
        + "        # Append final state as the last step\n"
        + "        TRACE_DATA.append({\n"
        + "            'step': STEP + 1,\n"
        + "            'line': USER_CODE_END - USER_CODE_START + 1,\n"
        + "            'function': '<module>',\n"
        + "            'event': 'final',\n"
        + "            'call_stack_depth': 0,\n"
        + "            'variables': _final_vars\n"
        + "        })\n"
        + "    \n"
        + "    sys.settrace(None)\n"
        + '    print("__TRACE_START__")\n'
        + "    try:\n"
        + "        print(json.dumps(TRACE_DATA))\n"
        + "    except Exception:\n"
        + '        print("[]")\n'
        + '    print("__TRACE_END__")\n'
    )

    return injected


def extract_trace(stdout: str) -> tuple[list[dict], str, str | None]:
    """
    Parses the sentinel-wrapped output produced by the injected harness.

    Returns:
        (trace_steps, program_output, exception_text | None)
    """
    exception_text: str | None = None
    program_output: str = stdout

    # Extract exception block if present
    if "__TRACE_EXCEPTION__" in stdout:
        parts = stdout.split("__TRACE_EXCEPTION__", 1)
        program_output = parts[0]
        remainder = parts[1]
        # The rest up to __TRACE_START__ (if present) is the traceback
        if "__TRACE_START__" in remainder:
            exception_text = remainder.split("__TRACE_START__")[0].strip()
        else:
            exception_text = remainder.strip()

    # Extract trace JSON block
    if "__TRACE_START__" not in stdout:
        return [], program_output.strip(), exception_text

    trace_raw = (
        stdout.split("__TRACE_START__")[1]
        .split("__TRACE_END__")[0]
        .strip()
    )

    # program_output is everything before __TRACE_START__ (and before any exception marker)
    pre_trace = stdout.split("__TRACE_START__")[0]
    if "__TRACE_EXCEPTION__" in pre_trace:
        program_output = pre_trace.split("__TRACE_EXCEPTION__")[0].strip()
    else:
        program_output = pre_trace.strip()

    try:
        trace_steps: list[dict] = json.loads(trace_raw)
    except json.JSONDecodeError:
        trace_steps = []

    return trace_steps, program_output, exception_text
