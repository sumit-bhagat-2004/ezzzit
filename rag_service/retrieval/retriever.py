"""
Retrieval module for semantic similarity search.
Uses Snowflake's vector similarity functions to find relevant knowledge chunks.
"""

import sys
import os
import logging
from typing import List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from db.snowflake_conn import get_cursor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def retrieve(query: str, top_k: int = None) -> List[str]:
    """
    Retrieve relevant knowledge chunks using semantic similarity search.
    
    Uses Snowflake's VECTOR_COSINE_SIMILARITY function to find chunks
    most similar to the query embedding.
    
    Args:
        query: Search query string
        top_k: Number of results to return (default from config)
    
    Returns:
        List of relevant content strings
    """
    if top_k is None:
        top_k = config.TOP_K_RESULTS
    
    cursor = get_cursor()
    
    try:
        # Query using vector similarity with Cortex embeddings
        # Orders by cosine similarity in descending order (most similar first)
        similarity_query = """
        SELECT 
            CONTENT,
            CONCEPT,
            VECTOR_COSINE_SIMILARITY(
                EMBEDDING,
                SNOWFLAKE.CORTEX.EMBED_TEXT_768('snowflake-arctic-embed-m', %(query)s)
            ) AS similarity_score
        FROM KNOWLEDGE_BASE
        ORDER BY similarity_score DESC
        LIMIT %(top_k)s
        """
        
        params = {
            'query': query,
            'top_k': top_k
        }
        
        logger.info(f"Executing similarity search for query: '{query}'")
        cursor.execute(similarity_query, params)
        
        results = cursor.fetchall()
        
        if not results:
            logger.warning(f"No results found for query: '{query}'")
            return []
        
        # Extract content from results
        # Results are tuples: (CONTENT, CONCEPT, similarity_score)
        content_list = [row[0] for row in results]
        
        logger.info(f"Retrieved {len(content_list)} chunks for query: '{query}'")
        
        # Log similarity scores for debugging
        for i, row in enumerate(results):
            logger.debug(f"Result {i+1}: concept={row[1]}, similarity={row[2]:.4f}")
        
        return content_list
    
    except Exception as e:
        logger.error(f"Error during retrieval: {e}")
        raise
    
    finally:
        cursor.close()


def retrieve_with_metadata(query: str, top_k: int = None) -> List[dict]:
    """
    Retrieve relevant knowledge chunks with metadata.
    
    Args:
        query: Search query string
        top_k: Number of results to return
    
    Returns:
        List of dictionaries with content, concept, and similarity score
    """
    if top_k is None:
        top_k = config.TOP_K_RESULTS
    
    cursor = get_cursor()
    
    try:
        similarity_query = """
        SELECT 
            ID,
            CONTENT,
            CONCEPT,
            VECTOR_COSINE_SIMILARITY(
                EMBEDDING,
                SNOWFLAKE.CORTEX.EMBED_TEXT_768('snowflake-arctic-embed-m', %(query)s)
            ) AS similarity_score
        FROM KNOWLEDGE_BASE
        ORDER BY similarity_score DESC
        LIMIT %(top_k)s
        """
        
        params = {
            'query': query,
            'top_k': top_k
        }
        
        cursor.execute(similarity_query, params)
        results = cursor.fetchall()
        
        if not results:
            return []
        
        # Build result dictionaries
        result_list = []
        for row in results:
            result_list.append({
                'id': row[0],
                'content': row[1],
                'concept': row[2],
                'similarity_score': float(row[3])
            })
        
        return result_list
    
    except Exception as e:
        logger.error(f"Error during retrieval with metadata: {e}")
        raise
    
    finally:
        cursor.close()