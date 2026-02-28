from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from models.request_models import CodeRequest, ExecuteResponse, TraceStep, AIAnalysis
from services.injector import inject_python_tracer, extract_trace
from services.judge0_client import send_to_judge0, decode_judge0_field
from services.gemini_service import get_gemini_service

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ezzzit – Code Trace API",
    description="Executes Python code via Judge0 and returns a full execution trace.",
    version="0.1.0",
)

# ─── CORS ─────────────────────────────────────────────────────────────────────
# Adjust origins when deploying; wildcard is fine for the hackathon.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Health check ─────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok"}


# ─── Execute endpoint ──────────────────────────────────────────────────────────
@app.post("/execute", response_model=ExecuteResponse)
def execute_code(req: CodeRequest):
    """
    Accepts Python source code, wraps it with the sys.settrace harness,
    submits to Judge0, and returns:
      - program stdout  (output)
      - full trace list (trace)
      - total steps     (steps)
      - exception text  (exception, if any)
    """
    if req.language != "python":
        raise HTTPException(
            status_code=400,
            detail="Only 'python' is supported for deep trace mode."
        )

    # 1️⃣  Inject tracer
    try:
        instrumented = inject_python_tracer(req.code)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    # 2️⃣  Send to Judge0
    judge_response = send_to_judge0(instrumented, stdin=req.stdin)

    if "error" in judge_response:
        raise HTTPException(status_code=502, detail=judge_response["error"])

    # 3️⃣  Decode stdout / stderr from Judge0
    stdout = decode_judge0_field(judge_response.get("stdout"))
    stderr = decode_judge0_field(judge_response.get("stderr"))
    compile_output = decode_judge0_field(judge_response.get("compile_output"))

    # Bubble up compile errors immediately
    if compile_output:
        raise HTTPException(
            status_code=422,
            detail=f"Compile error:\n{compile_output}"
        )

    # 4️⃣  Extract trace and clean program output
    trace_steps, program_output, exception_text = extract_trace(stdout)

    # Append stderr to output so the frontend can show it
    if stderr:
        program_output = (program_output + "\n[stderr]\n" + stderr).strip()

    # 5️⃣  Get AI analysis from Gemini (non-blocking - returns None on failure)
    ai_analysis = None
    if trace_steps:  # Only analyze if we have trace data
        try:
            logger.info("Starting Gemini analysis...")
            gemini_service = get_gemini_service()
            ai_result = gemini_service.analyze_execution(
                code=req.code,
                language=req.language,
                trace_data=trace_steps,
                output=program_output
            )
            if ai_result:
                ai_analysis = AIAnalysis(**ai_result)
                logger.info("Gemini analysis completed successfully")
        except Exception as e:
            logger.error(f"Gemini analysis failed: {e}")
            # Don't fail the whole request if AI fails
            pass

    return ExecuteResponse(
        output=program_output,
        trace=[TraceStep(**step) for step in trace_steps],
        steps=len(trace_steps),
        exception=exception_text,
        ai_analysis=ai_analysis,
    )
