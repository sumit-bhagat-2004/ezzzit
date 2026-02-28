"""
Document chunking module.
Splits text documents into overlapping chunks for optimal retrieval.
"""

import config
from typing import List


def split_into_words(text: str) -> List[str]:
    """
    Split text into words.
    
    Args:
        text: Input text string
    
    Returns:
        List of words
    """
    return text.split()


def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
    """
    Split text into overlapping chunks based on word count.
    
    Args:
        text: Input text to chunk
        chunk_size: Number of words per chunk (default from config)
        overlap: Number of overlapping words between chunks (default from config)
    
    Returns:
        List of text chunks
    """
    if chunk_size is None:
        chunk_size = config.CHUNK_SIZE
    
    if overlap is None:
        overlap = config.CHUNK_OVERLAP
    
    # Split text into words
    words = split_into_words(text)
    
    # If text is shorter than chunk size, return as single chunk
    if len(words) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(words):
        # Get chunk of words
        end = start + chunk_size
        chunk_words = words[start:end]
        
        # Join words back into text
        chunk = ' '.join(chunk_words)
        chunks.append(chunk)
        
        # Move start position, accounting for overlap
        start = end - overlap
        
        # Prevent infinite loop if overlap >= chunk_size
        if start <= (len(chunks) - 1) * (chunk_size - overlap):
            start = (len(chunks)) * (chunk_size - overlap)
        
        # Break if we've reached the end
        if end >= len(words):
            break
    
    return chunks


def chunk_document(content: str, concept: str = None) -> List[dict]:
    """
    Chunk a document and prepare it for ingestion.
    
    Args:
        content: Document content
        concept: Concept/topic name for the document
    
    Returns:
        List of dictionaries with chunk metadata
    """
    chunks = chunk_text(content)
    
    result = []
    for i, chunk in enumerate(chunks):
        result.append({
            'chunk_index': i,
            'concept': concept or 'unknown',
            'content': chunk,
            'word_count': len(split_into_words(chunk))
        })
    
    return result