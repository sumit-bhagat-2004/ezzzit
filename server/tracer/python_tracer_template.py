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

        local_vars = {}
        for k, v in frame.f_locals.items():
            if k in _HARNESS_VARS or k.startswith("__"):
                continue  # skip harness internals and dunder names
            try:
                json.dumps(v)
                local_vars[k] = v
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
