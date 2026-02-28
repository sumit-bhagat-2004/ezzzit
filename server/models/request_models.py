from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Dict


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


class DataStructure(BaseModel):
    name: str
    type: str
    variables: List[str]
    description: str


class AIAnalysis(BaseModel):
    structures: List[DataStructure]
    trace_enrichment: Dict[str, Dict[str, str]]  # {"step_index_mapping": {"1": "explanation"}}
    summary: str


class ExecuteResponse(BaseModel):
    output: str
    trace: list[TraceStep]
    steps: int
    exception: str | None = None
    error: str | None = None
    ai_analysis: Optional[AIAnalysis] = None  # Added AI analysis field
