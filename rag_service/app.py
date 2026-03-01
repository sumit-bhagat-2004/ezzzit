"""
FastAPI application for Snowflake RAG Service.
Exposes retrieval endpoint for semantic knowledge search.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import List, Dict, Any
import logging

import config
from retrieval.retriever import retrieve, retrieve_with_metadata, clean_content, extract_key_sentences, retrieve_by_concept
from db.snowflake_conn import get_connection, close_connection
import re
import httpx
from explainer.step_explainer import StepExplainer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Snowflake RAG Service",
    description="Retrieval Augmented Generation service using Snowflake vector search",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods including OPTIONS
    allow_headers=["*"],  # Allows all headers
)


def split_into_sentences(text: str) -> list:
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    return [s.strip() for s in sentences if s.strip()]


# Request/Response models
class RetrievalRequest(BaseModel):
    """Request model for knowledge retrieval."""
    query: str
    top_k: int = 3

    class Config:
        json_schema_extra = {
            "example": {
                "query": "loop iteration",
                "top_k": 3
            }
        }


class RetrievalResponse(BaseModel):
    """Response model for knowledge retrieval."""
    knowledge: List[str]
    query: str
    count: int

    class Config:
        json_schema_extra = {
            "example": {
                "knowledge": [
                    "Loops allow you to execute code repeatedly...",
                    "For loops iterate over sequences...",
                    "While loops continue until condition is false..."
                ],
                "query": "loop iteration",
                "count": 3
            }
        }


class RetrievalDetailResponse(BaseModel):
    """Detailed response model with metadata."""
    results: List[dict]
    query: str
    count: int


class CleanRetrievalResponse(BaseModel):
    """Clean, formatted response without code blocks."""
    summaries: List[str]
    query: str
    count: int

    class Config:
        json_schema_extra = {
            "example": {
                "summaries": [
                    "Recursion is a programming technique where a function calls itself to solve problems.",
                    "A recursive function has two essential components: base case and recursive case.",
                    "Recursion is particularly well-suited for tree traversal and divide-and-conquer algorithms."
                ],
                "query": "what is recursion?",
                "count": 3
            }
        }


class StepByStepResponse(BaseModel):
    """Step-by-step explanation response."""
    topic: str
    explanation: str
    key_points: List[str]
    query: str

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Loops",
                "explanation": "Loops are control structures that execute code repeatedly. For loops iterate over sequences when you know the iteration count. While loops continue until a condition becomes false...",
                "key_points": [
                    "For loops: Used when iteration count is known",
                    "While loops: Continue until condition is false",
                    "Loop control: Use break to exit, continue to skip",
                    "Nested loops: Loop inside another loop"
                ],
                "query": "how loops work"
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    message: str


# Trace Explanation Models
class TraceExplainRequest(BaseModel):
    """Request model for trace-based explanation."""
    code: str
    language: str = "python"
    stdin: str = ""
    level: str = "medium"

    @field_validator('level')
    @classmethod
    def validate_level(cls, v: str) -> str:
        """Validate and normalize the level parameter."""
        normalized = v.lower()
        valid_levels = ["beginner", "medium", "interview_ready"]
        if normalized not in valid_levels:
            raise ValueError(f"Level must be one of {valid_levels}, got '{v}'")
        return normalized

    class Config:
        json_schema_extra = {
            "example": {
                "code": "a = 5\nb = 3\nsum_val = a + b\nprint(sum_val)",
                "language": "python",
                "stdin": "",
                "level": "medium"
            }
        }


class EnrichedTraceStep(BaseModel):
    """Single enriched trace step with explanation."""
    step: int
    line: int
    variables: Dict[str, Any]
    explanation: str


class TraceExplainResponse(BaseModel):
    """Response model for trace explanation."""
    output: str
    trace: List[EnrichedTraceStep]

    class Config:
        json_schema_extra = {
            "example": {
                "output": "8",
                "trace": [
                    {
                        "step": 1,
                        "line": 1,
                        "variables": {"a": 5},
                        "explanation": "Variable `a` is created with value `5`."
                    },
                    {
                        "step": 2,
                        "line": 2,
                        "variables": {"a": 5, "b": 3},
                        "explanation": "Variable `b` is created with value `3`."
                    },
                    {
                        "step": 3,
                        "line": 3,
                        "variables": {"a": 5, "b": 3, "sum_val": 8},
                        "explanation": "Executing line 3: `sum_val = a + b`. Variable `sum_val` is created with value `8`. Variables a and b are added to compute sum_val."
                    }
                ]
            }
        }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup."""
    try:
        logger.info("Starting Snowflake RAG Service...")
        config.validate_config()

        # Test connection
        conn = get_connection()
        logger.info("Snowflake connection successful")

    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Close connections on shutdown."""
    try:
        close_connection()
        logger.info("Snowflake RAG Service stopped")
    except Exception as e:
        logger.error(f"Shutdown error: {e}")


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify service is running.
    """
    try:
        # Test Snowflake connection
        conn = get_connection()

        if conn.is_closed():
            raise HTTPException(status_code=503, detail="Snowflake connection is closed")

        return HealthResponse(
            status="healthy",
            message="Service is running and connected to Snowflake"
        )

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


# Main retrieval endpoint
@app.post("/rag/retrieve", response_model=RetrievalResponse)
async def retrieve_knowledge(request: RetrievalRequest):
    """
    Retrieve relevant knowledge chunks using semantic similarity search.

    Args:
        request: RetrievalRequest with query string

    Returns:
        RetrievalResponse with list of relevant knowledge chunks
    """
    try:
        logger.info(f"Received retrieval request: '{request.query}'")

        # Validate query
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # Perform retrieval
        knowledge_chunks = retrieve(request.query, top_k=request.top_k)

        # Handle empty results
        if not knowledge_chunks:
            logger.warning(f"No results found for query: '{request.query}'")
            return RetrievalResponse(
                knowledge=[],
                query=request.query,
                count=0
            )

        logger.info(f"Retrieved {len(knowledge_chunks)} chunks for query: '{request.query}'")

        return RetrievalResponse(
            knowledge=knowledge_chunks,
            query=request.query,
            count=len(knowledge_chunks)
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Retrieval error: {e}")
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")


# Detailed retrieval endpoint with metadata
@app.post("/rag/retrieve/detailed", response_model=RetrievalDetailResponse)
async def retrieve_knowledge_detailed(request: RetrievalRequest):
    """
    Retrieve relevant knowledge chunks with metadata (concept, similarity score).

    Args:
        request: RetrievalRequest with query string

    Returns:
        RetrievalDetailResponse with results including metadata
    """
    try:
        logger.info(f"Received detailed retrieval request: '{request.query}'")

        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        results = retrieve_with_metadata(request.query, top_k=request.top_k)

        return RetrievalDetailResponse(
            results=results,
            query=request.query,
            count=len(results)
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Detailed retrieval error: {e}")
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")


# Clean retrieval endpoint (recommended)
@app.post("/rag/retrieve/clean", response_model=CleanRetrievalResponse)
async def retrieve_knowledge_clean(request: RetrievalRequest):
    """
    Retrieve relevant knowledge with clean formatting.
    Removes code blocks and returns concise summaries.

    Args:
        request: RetrievalRequest with query string

    Returns:
        CleanRetrievalResponse with formatted summaries
    """
    try:
        logger.info(f"Received clean retrieval request: '{request.query}'")

        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # Retrieve raw chunks
        knowledge_chunks = retrieve(request.query, top_k=request.top_k)

        if not knowledge_chunks:
            return CleanRetrievalResponse(
                summaries=[],
                query=request.query,
                count=0
            )

        # Clean and format each chunk
        summaries = []
        for chunk in knowledge_chunks:
            # Extract key sentences (more focused)
            summary = extract_key_sentences(chunk, num_sentences=2)
            # Clean markdown and code
            clean_summary = clean_content(summary, max_length=250)
            summaries.append(clean_summary)

        logger.info(f"Retrieved and cleaned {len(summaries)} summaries")

        return CleanRetrievalResponse(
            summaries=summaries,
            query=request.query,
            count=len(summaries)
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Clean retrieval error: {e}")
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")


# Step-by-step explanation endpoint
@app.post("/rag/explain", response_model=StepByStepResponse)
async def explain_topic(request: RetrievalRequest):
    """
    Get a structured step-by-step explanation of a topic.
    Combines multiple knowledge chunks into a coherent explanation.

    Args:
        request: RetrievalRequest with topic query

    Returns:
        StepByStepResponse with structured explanation
    """
    try:
        logger.info(f"Received explanation request: '{request.query}'")

        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # Retrieve using concept-aware search for better relevance
        top_k = max(request.top_k, 5)  # Get at least 5 chunks
        knowledge_chunks = retrieve_by_concept(request.query, top_k=top_k)

        if not knowledge_chunks:
            raise HTTPException(status_code=404, detail="No knowledge found for this topic")

        # Extract topic name from query
        topic = request.query.replace("how", "").replace("what is", "").replace("explain", "").replace("teach me", "").strip().title()
        if not topic or len(topic) < 3:
            # Try to detect from content
            query_lower = request.query.lower()
            if 'array' in query_lower or 'list' in query_lower:
                topic = "Arrays and Lists"
            elif 'loop' in query_lower or 'iterate' in query_lower:
                topic = "Loops"
            elif 'recurs' in query_lower:
                topic = "Recursion"
            else:
                topic = "Programming Concept"

        # Build comprehensive explanation from multiple chunks
        all_text = "\n\n".join(knowledge_chunks)

        # Clean the combined text
        explanation = clean_content(all_text, max_length=800)

        # Extract key points (look for bullet points, numbered lists, or important sentences)
        key_points = []

        for chunk in knowledge_chunks[:4]:  # Use top 4 chunks for key points
            # Look for list items or important statements
            lines = chunk.split('\n')
            for line in lines:
                line = line.strip()

                # Match bullet points or numbered lists
                if re.match(r'^[-*+]\s+', line) or re.match(r'^\d+\.\s+', line):
                    # Clean the line
                    point = re.sub(r'^[-*+\d.]\s+', '', line)
                    point = clean_content(point, max_length=150)
                    if point and len(point) > 15 and point not in key_points:
                        key_points.append(point)

                # Match sentences with keywords indicating importance
                elif any(kw in line.lower() for kw in ['is used', 'allows', 'enables', 'helps', 'important', 'essential', 'are', 'can', 'provides']):
                    if len(line) > 30 and len(line) < 300:  # Reasonable length
                        point = clean_content(line, max_length=150)
                        if point and len(point) > 15 and point not in key_points:
                            key_points.append(point)

                if len(key_points) >= 8:
                    break

            if len(key_points) >= 8:
                break

        # If still not enough key points, extract first sentences
        if len(key_points) < 3:
            for chunk in knowledge_chunks[:4]:
                sentences = split_into_sentences(chunk)
                for sent in sentences[:2]:  # First 2 sentences from each chunk
                    if len(sent) > 30:
                        point = clean_content(sent, max_length=150)
                        if point and point not in key_points:
                            key_points.append(point)
                        if len(key_points) >= 6:
                            break
                if len(key_points) >= 6:
                    break

        logger.info(f"Generated explanation with {len(key_points)} key points for topic: {topic}")

        return StepByStepResponse(
            topic=topic,
            explanation=explanation,
            key_points=key_points[:6],  # Max 6 key points
            query=request.query
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Explanation error: {e}")
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")


# Trace-aware explanation endpoint (NEW)
@app.post("/rag/explain_trace", response_model=TraceExplainResponse)
async def explain_trace(request: TraceExplainRequest):
    """
    Generate step-by-step explanations for execution traces.

    This endpoint:
    1. Calls external execution API to get trace
    2. Processes trace and computes state differences
    3. Extracts runtime concepts
    4. Retrieves relevant knowledge from Snowflake
    5. Generates grounded explanations for each step

    Args:
        request: TraceExplainRequest with code, language, and stdin

    Returns:
        TraceExplainResponse with output and enriched trace
    """
    try:
        logger.info(f"Received trace explanation request for {len(request.code)} chars of {request.language} code")

        # Validate input
        if not request.code or not request.code.strip():
            raise HTTPException(status_code=400, detail="Code cannot be empty")

        if request.language.lower() != "python":
            raise HTTPException(status_code=400, detail="Currently only Python is supported")

        # Step 1: Call external execution API
        execution_api_url = f"{config.EXECUTION_API_URL}/execute"

        execution_payload = {
            "code": request.code,
            "language": request.language,
            "stdin": request.stdin
        }

        logger.info(f"Calling execution API at {execution_api_url}")

        async with httpx.AsyncClient(timeout=30.0) as client:
            execution_response = await client.post(execution_api_url, json=execution_payload)

        if execution_response.status_code != 200:
            logger.error(f"Execution API error: {execution_response.status_code}")
            raise HTTPException(
                status_code=502,
                detail=f"Execution API failed with status {execution_response.status_code}"
            )

        execution_data = execution_response.json()
        logger.info(f"Received execution response with trace")

        # Extract output and trace
        output = execution_data.get("output", "")
        raw_trace = execution_data.get("trace", [])

        if not raw_trace:
            logger.warning("Empty trace received from execution API")
            # Return minimal response
            return TraceExplainResponse(
                output=output,
                trace=[]
            )

        logger.info(f"Processing {len(raw_trace)} trace steps")

        # Step 2-6: Generate explanations using StepExplainer with level
        explainer = StepExplainer(top_k_knowledge=3, level=request.level)
        enriched_steps = explainer.generate_step_explanations(request.code, raw_trace)

        logger.info(f"Generated {len(enriched_steps)} enriched trace steps at {request.level} level")

        # Convert to response model
        trace_steps = [
            EnrichedTraceStep(**step) for step in enriched_steps
        ]

        return TraceExplainResponse(
            output=output,
            trace=trace_steps
        )

    except HTTPException:
        raise

    except httpx.TimeoutException:
        logger.error("Execution API timeout")
        raise HTTPException(status_code=504, detail="Execution API timeout")

    except httpx.RequestError as e:
        logger.error(f"Execution API connection error: {e}")
        raise HTTPException(status_code=502, detail=f"Cannot connect to execution API: {str(e)}")

    except Exception as e:
        logger.error(f"Trace explanation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Trace explanation failed: {str(e)}")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "Snowflake RAG Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "retrieve": "/rag/retrieve",
            "retrieve_clean": "/rag/retrieve/clean",
            "explain": "/rag/explain (step-by-step explanations)",
            "explain_trace": "/rag/explain_trace (trace-aware explanations with levels)",
            "retrieve_detailed": "/rag/retrieve/detailed",
            "docs": "/docs"
        },
        "recommendations": {
            "quick_facts": "Use /rag/retrieve/clean",
            "learning": "Use /rag/explain for step-by-step",
            "code_execution": "Use /rag/explain_trace for execution traces"
        },
        "explain_trace_levels": {
            "beginner": "Easiest explanations for learning programming",
            "medium": "Standard explanations (default)",
            "interview_ready": "Technical explanations for interview prep"
        }
    }
