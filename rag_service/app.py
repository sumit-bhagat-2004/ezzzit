"""
FastAPI application for Snowflake RAG Service.
Exposes retrieval endpoint for semantic knowledge search.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging

import config
from retrieval.retriever import retrieve, retrieve_with_metadata
from db.snowflake_conn import get_connection, close_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Snowflake RAG Service",
    description="Retrieval Augmented Generation service using Snowflake vector search",
    version="1.0.0"
)


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


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    message: str


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
            "retrieve_detailed": "/rag/retrieve/detailed",
            "docs": "/docs"
        }
    }