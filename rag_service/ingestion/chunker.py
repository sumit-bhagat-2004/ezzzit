"""
Document chunking module.
Splits text documents into overlapping chunks for optimal retrieval.
"""

import config
from typing import List
import re


def clean_markdown(text: str) -> str:
    """
    Clean markdown text by removing excessive formatting but keeping structure.
    
    Args:
        text: Input markdown text
    
    Returns:
        Cleaned text
    """
    # Remove multiple blank lines
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    return text.strip()


def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences for better chunking.
    
    Args:
        text: Input text
    
    Returns:
        List of sentences
    """
    # Split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_by_paragraph(text: str, max_words: int = 200) -> List[str]:
    """
    Chunk text by paragraphs and logical sections.
    Better preserves context than word-based chunking.
    
    Args:
        text: Input text
        max_words: Maximum words per chunk
    
    Returns:
        List of text chunks
    """
    chunks = []
    
    # Split by double newlines (paragraphs)
    paragraphs = text.split('\n\n')
    
    current_chunk = []
    current_word_count = 0
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        para_words = len(para.split())
        
        # If this paragraph alone exceeds max, split it further
        if para_words > max_words:
            # Save current chunk if exists
            if current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = []
                current_word_count = 0
            
            # Split long paragraph by sentences
            sentences = split_into_sentences(para)
            temp_chunk = []
            temp_count = 0
            
            for sent in sentences:
                sent_words = len(sent.split())
                if temp_count + sent_words > max_words and temp_chunk:
                    chunks.append(' '.join(temp_chunk))
                    temp_chunk = [sent]
                    temp_count = sent_words
                else:
                    temp_chunk.append(sent)
                    temp_count += sent_words
            
            if temp_chunk:
                chunks.append(' '.join(temp_chunk))
        
        # If adding this paragraph exceeds max, save current chunk
        elif current_word_count + para_words > max_words and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_word_count = para_words
        
        # Add paragraph to current chunk
        else:
            current_chunk.append(para)
            current_word_count += para_words
    
    # Add remaining chunk
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks


def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
    """
    Split text into overlapping chunks with improved logic.
    
    Args:
        text: Input text to chunk
        chunk_size: Target number of words per chunk (default from config)
        overlap: Not used in new implementation
    
    Returns:
        List of text chunks
    """
    if chunk_size is None:
        chunk_size = config.CHUNK_SIZE
    
    # Clean the text first
    text = clean_markdown(text)
    
    # Use paragraph-based chunking for better context preservation
    chunks = chunk_by_paragraph(text, max_words=chunk_size)
    
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
        if len(chunk.split()) < 20:
            continue
        
        result.append({
            'chunk_index': i,
            'concept': concept or 'unknown',
            'content': chunk,
            'word_count': len(chunk.split())
        })
    
    return result