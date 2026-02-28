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

    The final output on stdout will look like:
        <program output>
        __TRACE_START__
        [{ ...trace steps... }]
        __TRACE_END__

    If the user code raises an exception:
        __TRACE_EXCEPTION__
        <traceback>
    """
    if len(user_code.splitlines()) > MAX_CODE_LINES:
        raise ValueError(
            f"Code exceeds the {MAX_CODE_LINES}-line limit "
            f"({len(user_code.splitlines())} lines submitted)."
        )

    tracer_src = _TRACER_PATH.read_text(encoding="utf-8")

    injected = f"""{tracer_src}

# ─── User code ───────────────────────────────────────────────────────────────
try:
{_indent(user_code)}
except Exception as _exc:
    import traceback as _tb
    print("__TRACE_EXCEPTION__")
    print(_tb.format_exc())
finally:
    sys.settrace(None)
    print("__TRACE_START__")
    print(json.dumps(TRACE_DATA))
    print("__TRACE_END__")
"""
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
