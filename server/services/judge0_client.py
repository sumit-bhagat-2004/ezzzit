import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

JUDGE0_URL = os.getenv("JUDGE0_URL", "http://localhost:2358")
PYTHON_LANGUAGE_ID = 71  # CPython 3 on Judge0

# Execution limits – keeps demos stable during the hackathon
CPU_TIME_LIMIT = 3      # seconds
WALL_TIME_LIMIT = 5     # seconds
MEMORY_LIMIT = 128_000  # KB  (~128 MB)


def send_to_judge0(code: str, stdin: str = "") -> dict:
    """
    Encodes *code* in base64 and submits it to Judge0 in synchronous (wait)
    mode.  Returns the raw Judge0 response dict.
    """
    endpoint = f"{JUDGE0_URL}/submissions?base64_encoded=true&wait=true"

    encoded_code = base64.b64encode(code.encode()).decode()
    encoded_stdin = base64.b64encode(stdin.encode()).decode()

    payload = {
        "language_id": PYTHON_LANGUAGE_ID,
        "source_code": encoded_code,
        "stdin": encoded_stdin,
        "cpu_time_limit": CPU_TIME_LIMIT,
        "wall_time_limit": WALL_TIME_LIMIT,
        "memory_limit": MEMORY_LIMIT,
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": f"Cannot connect to Judge0 at {JUDGE0_URL}. Is it running?"}
    except requests.exceptions.Timeout:
        return {"error": "Judge0 request timed out."}
    except requests.exceptions.HTTPError as exc:
        return {"error": f"Judge0 HTTP error: {exc}"}


def decode_judge0_field(value: str | None) -> str:
    """Base64-decode a Judge0 response field, returning '' for None/empty."""
    if not value:
        return ""
    try:
        return base64.b64decode(value.encode()).decode(errors="replace")
    except Exception:
        return value  # already plain text (shouldn't happen in b64 mode)
