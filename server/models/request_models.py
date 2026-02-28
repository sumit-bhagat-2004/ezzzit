from pydantic import BaseModel, Field
from typing import Literal


class CodeRequest(BaseModel):
    code: str = Field(..., description="The source code to execute and trace")
    language: Literal["python"] = Field(
        default="python",
        description="Programming language (only 'python' supported for deep trace)"
    )
    stdin: str = Field(default="", description="Optional stdin input for the program")


class TraceStep(BaseModel):
    step: int
    line: int
    function: str
    event: str
    call_stack_depth: int
    variables: dict


class ExecuteResponse(BaseModel):
    output: str
    trace: list[TraceStep]
    steps: int
    exception: str | None = None
    error: str | None = None
