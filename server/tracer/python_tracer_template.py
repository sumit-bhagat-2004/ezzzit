import sys
import json

# ─── Guardrails ───────────────────────────────────────────────────────────────
MAX_STEPS = 200

# ─── Trace state ──────────────────────────────────────────────────────────────
TRACE_DATA = []
STEP = 0
CALL_STACK = 0

# Set by the injector BEFORE sys.settrace is called.
# These are absolute line numbers in the fully-assembled script (1-indexed).
# The tracer only records events that fall inside [USER_CODE_START, USER_CODE_END].
USER_CODE_START = 0
USER_CODE_END = 0

# Variables introduced by the harness itself.
# At module level locals() == globals(), so without this filter TRACE_DATA
# would be captured inside its own entries -> circular reference -> MemoryError.
_HARNESS_VARS = frozenset({
    "sys", "json",
    "MAX_STEPS", "TRACE_DATA", "STEP", "CALL_STACK",
    "USER_CODE_START", "USER_CODE_END",
    "tracer", "_HARNESS_VARS",
    "_exc", "_tb",   # injected except-clause names
})


def tracer(frame, event, arg):
    global STEP, CALL_STACK

    # ── Track call depth for user-defined functions only ──────────────────────
    if event == "call":
        if USER_CODE_START <= frame.f_lineno <= USER_CODE_END:
            CALL_STACK += 1
        return tracer

    if event == "return":
        if USER_CODE_START <= frame.f_lineno <= USER_CODE_END:
            CALL_STACK = max(0, CALL_STACK - 1)
        return tracer

    # ── Only record line / exception events inside user code ──────────────────
    if event in ("line", "exception"):
        lineno = frame.f_lineno

        if not (USER_CODE_START <= lineno <= USER_CODE_END):
            return tracer

        # Hard-stop: disable tracer once step limit is reached
        if STEP >= MAX_STEPS:
            sys.settrace(None)
            return None

        STEP += 1

        # Normalise to user-code line numbers (user line 1 == USER_CODE_START)
        user_lineno = lineno - USER_CODE_START + 1

        # ─── HELPER: Recursive Serializer ─────────────────────────────────────
        def serialize(obj, depth=0, max_depth=3):
            if depth > max_depth:
                return "..."
            
            # Primitives
            if obj is None or isinstance(obj, (int, float, str, bool)):
                return obj
            
            # 1. Sets (Serialize as sorted list with type tag)
            if isinstance(obj, set):
                return {
                    "__type__": "set",
                    "items": [serialize(x, depth + 1) for x in sorted(list(obj), key=str)]
                }

            # 2. Deques (Queue support)
            if type(obj).__name__ == "deque":
                return {
                    "__type__": "deque",
                    "items": [serialize(x, depth + 1) for x in list(obj)]
                }
            
            # Lists/Tuples
            if isinstance(obj, (list, tuple)):
                return [serialize(x, depth + 1) for x in obj]
            
            # Dictionaries
            if isinstance(obj, dict):
                return {k: serialize(v, depth + 1) for k, v in obj.items()}
            
            # Objects (The Magic Part)
            if hasattr(obj, "__dict__"):
                return {
                    "__type__": type(obj).__name__,
                    "__id__": str(id(obj)), # Good for graph linking later
                    **{k: serialize(v, depth + 1) for k, v in vars(obj).items() if not k.startswith('_')}
                }
            
            return repr(obj)

        # ─── Capture Variables ────────────────────────────────────────────────
        local_vars = {}
        
        # At module level (function name '<module>'), capture both locals and globals
        # For functions, only capture locals
        if frame.f_code.co_name == "<module>":
            # Module-level: merge locals and globals (they're usually the same, but filter carefully)
            all_vars = {**frame.f_globals, **frame.f_locals}
            for k, v in all_vars.items():
                if k in _HARNESS_VARS or k.startswith("__"):
                    continue
                # Skip built-in modules and functions
                if callable(v) and hasattr(v, "__module__"):
                    if v.__module__ in ("builtins", "sys", "json"):
                        continue
                
                try:
                    local_vars[k] = serialize(v)
                except Exception:
                    local_vars[k] = repr(v)
        else:
            # Function-level: only capture locals
            for k, v in frame.f_locals.items():
                if k in _HARNESS_VARS or k.startswith("__"):
                    continue
                
                try:
                    local_vars[k] = serialize(v)
                except Exception:
                    local_vars[k] = repr(v)

        TRACE_DATA.append(
            {
                "step": STEP,
                "line": user_lineno,
                "function": frame.f_code.co_name,
                "event": event,
                "call_stack_depth": CALL_STACK,
                "variables": local_vars,
            }
        )

    return tracer


# sys.settrace(tracer) is intentionally NOT called here.
# The injector sets USER_CODE_START / USER_CODE_END first, then activates
# the tracer so the range filter is correct from the very first event.
