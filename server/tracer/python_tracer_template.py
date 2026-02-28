import sys
import json

# ─── Guardrails ───────────────────────────────────────────────────────────────
MAX_STEPS = 200

# ─── Trace state ──────────────────────────────────────────────────────────────
TRACE_DATA = []
STEP = 0
CALL_STACK = 0


def tracer(frame, event, arg):
    global STEP, CALL_STACK

    # Ignore frames from the tracer harness itself
    if frame.f_code.co_filename == "<string>" and frame.f_code.co_name in (
        "tracer",
        "<module>",
    ):
        # Still allow <module> to be traced but skip the harness functions
        if frame.f_code.co_name != "<module>":
            return tracer

    if event == "call":
        CALL_STACK += 1

    if event == "return":
        CALL_STACK -= 1

    if event in ("line", "call", "return", "exception"):
        # Hard-stop: unset tracer once limit is exceeded
        if STEP >= MAX_STEPS:
            sys.settrace(None)
            return None

        if event == "line":
            STEP += 1

        local_vars = {}
        for k, v in frame.f_locals.items():
            try:
                json.dumps(v)
                local_vars[k] = v
            except Exception:
                local_vars[k] = str(v)

        TRACE_DATA.append(
            {
                "step": STEP,
                "line": frame.f_lineno,
                "function": frame.f_code.co_name,
                "event": event,
                "call_stack_depth": CALL_STACK,
                "variables": local_vars,
            }
        )

    return tracer


sys.settrace(tracer)
