"""
Retrieval module for semantic similarity search.
Uses Snowflake's vector similarity functions to find relevant knowledge chunks.
"""

import sys
import os
import logging
import re
from typing import List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from db.snowflake_conn import get_cursor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_content(content: str, max_length: int = 300) -> str:
    """
    Clean and format content for better readability.
    Removes code blocks, excessive whitespace, and truncates if needed.
    
    Args:
        content: Raw content string
        max_length: Maximum character length
    
    Returns:
        Cleaned content string
    """
    # Remove code blocks (anything between triple backticks)
    content = re.sub(r'```[\s\S]*?```', '', content)
    
    # Remove inline code
    content = re.sub(r'`[^`]+`', '', content)
    
    # Remove markdown headers (## ### etc)
    content = re.sub(r'^#{1,6}\s+', '', content, flags=re.MULTILINE)
    
    # Remove markdown bold/italic
    content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
    content = re.sub(r'\*([^*]+)\*', r'\1', content)
    
    # Remove bullet points and list markers
    content = re.sub(r'^\s*[-*+]\s+', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*\d+\.\s+', '', content, flags=re.MULTILINE)
    
    # Replace multiple newlines with single newline
    content = re.sub(r'\n\s*\n+', '\n', content)
    
    # Remove extra whitespace
    content = re.sub(r'\s+', ' ', content)
    
    # Trim
    content = content.strip()
    
    # Truncate if too long
    if len(content) > max_length:
        content = content[:max_length].rsplit(' ', 1)[0] + '...'
    
    return content


def extract_key_sentences(content: str, num_sentences: int = 2) -> str:
    """
    Extract the first N sentences from content.
    
    Args:
        content: Content string
        num_sentences: Number of sentences to extract
    
    Returns:
        First N sentences
    """
    # Split by sentence endings
    sentences = re.split(r'[.!?]+\s+', content)
    
    # Filter out empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Take first N sentences
    selected = sentences[:num_sentences]
    
    return '. '.join(selected) + '.'


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
    
    # Enhance query for better semantic matching
    enhanced_query = enhance_query(query)
    
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
            'query': enhanced_query,
            'top_k': top_k
        }
        
        logger.info(f"Executing similarity search for query: '{enhanced_query}'")
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
            logger.info(f"Result {i+1}: concept={row[1]}, similarity={row[2]:.4f}")
        
        return content_list
    
    except Exception as e:
        logger.error(f"Error during retrieval: {e}")
        raise
    
    finally:
        cursor.close()


def enhance_query(query: str) -> str:
    """
    Enhance query with context keywords for better semantic matching.
    
    Args:
        query: Original query string
    
    Returns:
        Enhanced query with additional context
    """
    query_lower = query.lower()
    
    # Add programming context
    enhancements = []
    
    # Array/List queries
    if any(word in query_lower for word in ['array', 'list', 'arrays', 'lists']):
        enhancements.append("arrays lists data structures indexing slicing")
    
    # Loop queries  
    elif any(word in query_lower for word in ['loop', 'loops', 'iterate', 'iteration']):
        enhancements.append("loops for while iteration control structures")
    
    # Recursion queries
    elif any(word in query_lower for word in ['recursion', 'recursive', 'recurs']):
        enhancements.append("recursion recursive functions base case")
    
    # Generic programming query
    if not enhancements:
        enhancements.append("programming python code")
    
    # Combine original query with enhancements
    enhanced = f"{query} {' '.join(enhancements)}"
    
    return enhanced


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
    
    enhanced_query = enhance_query(query)
    
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
            'query': enhanced_query,
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


def retrieve_by_concept(query: str, concept_hint: str = None, top_k: int = None) -> List[str]:
    """
    Retrieve knowledge with concept filtering for better relevance.
    
    Args:
        query: Search query
        concept_hint: Hint about the concept (arrays, loops, recursion)
        top_k: Number of results
    
    Returns:
        List of relevant content strings
    """
    if top_k is None:
        top_k = config.TOP_K_RESULTS
    
    # Detect concept from query if not provided
    if not concept_hint:
        query_lower = query.lower()
        if any(word in query_lower for word in ['array', 'list', 'arrays', 'lists']):
            concept_hint = 'arrays'
        elif any(word in query_lower for word in ['loop', 'loops', 'iterate']):
            concept_hint = 'loops'
        elif any(word in query_lower for word in ['recurs', 'recursive']):
            concept_hint = 'recursion'
    
    enhanced_query = enhance_query(query)
    cursor = get_cursor()
    
    try:
        if concept_hint:
            # Search with concept filter
            similarity_query = """
            SELECT 
                CONTENT,
                CONCEPT,
                VECTOR_COSINE_SIMILARITY(
                    EMBEDDING,
                    SNOWFLAKE.CORTEX.EMBED_TEXT_768('snowflake-arctic-embed-m', %(query)s)
                ) AS similarity_score
            FROM KNOWLEDGE_BASE
            WHERE LOWER(CONCEPT) = LOWER(%(concept)s)
            ORDER BY similarity_score DESC
            LIMIT %(top_k)s
            """
            
            params = {
                'query': enhanced_query,
                'concept': concept_hint,
                'top_k': top_k
            }
        else:
            # Fall back to regular search
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
                'query': enhanced_query,
                'top_k': top_k
            }
        
        logger.info(f"Searching with concept filter: {concept_hint}")
        cursor.execute(similarity_query, params)
        results = cursor.fetchall()
        
        if not results:
            logger.warning(f"No results for concept: {concept_hint}")
            return []
        
        content_list = [row[0] for row in results]
        
        # Log results
        for i, row in enumerate(results):
            logger.info(f"Result {i+1}: concept={row[1]}, similarity={row[2]:.4f}")
        
        return content_list
    
    except Exception as e:
        logger.error(f"Error in concept retrieval: {e}")
        raise
    
    finally:
        cursor.close()