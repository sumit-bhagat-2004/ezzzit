"""
Knowledge Retrieval Integration

Integrates runtime concepts with Snowflake vector retrieval.
Queries knowledge base using extracted concepts and executed code.

Uses existing retrieval/retriever.py module.
"""

import logging
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retrieval.retriever import retrieve, retrieve_by_concept, retrieve_with_metadata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KnowledgeRetriever:
    """Retrieves relevant knowledge for trace step explanation."""
    
    def __init__(self, top_k: int = 3):
        """
        Initialize knowledge retriever.
        
        Args:
            top_k: Number of knowledge chunks to retrieve per query
        """
        self.top_k = top_k
        logger.info(f"Initialized KnowledgeRetriever with top_k={top_k}")
    
    def _build_query(self, concepts: List[str], source_line: str) -> str:
        """
        Build retrieval query from concepts and source code.
        
        Args:
            concepts: List of extracted concept keywords
            source_line: Executed source code line
        
        Returns:
            Query string for vector retrieval
        """
        # Combine concepts with source line context
        concept_str = ' '.join(concepts)
        
        # Clean source line (remove extra whitespace, keep code essence)
        cleaned_source = ' '.join(source_line.split())
        
        # Build query prioritizing concepts
        if concepts:
            query = f"{concept_str} {cleaned_source}"
        else:
            query = cleaned_source
        
        logger.debug(f"Built query: {query}")
        return query
    
    def _select_primary_concept(self, concepts: List[str]) -> str:
        """
        Select the most relevant primary concept for focused retrieval.
        
        Prioritizes high-level concepts over low-level ones.
        
        Args:
            concepts: List of concept keywords
        
        Returns:
            Primary concept keyword, or None
        """
        # Priority order for concept selection
        priority_concepts = [
            'iteration',
            'conditional',
            'function_call',
            'recursion',
            'list_comprehension',
            'exception_handling',
            'dictionary',
            'list',
            'arithmetic',
            'assignment'
        ]
        
        for priority in priority_concepts:
            if priority in concepts:
                return priority
        
        # Return first concept if no priority match
        if concepts:
            return concepts[0]
        
        return None
    
    def retrieve_for_step(
        self, 
        concepts: List[str], 
        source_line: str,
        use_concept_filter: bool = True
    ) -> List[str]:
        """
        Retrieve relevant knowledge for a single trace step.
        
        Args:
            concepts: Extracted runtime concepts
            source_line: Executed source code line
            use_concept_filter: Whether to use concept-based filtering
        
        Returns:
            List of relevant knowledge chunks
        """
        if not concepts and not source_line:
            logger.warning("No concepts or source line provided")
            return []
        
        try:
            # Build query from concepts and source
            query = self._build_query(concepts, source_line)
            
            # Try concept-filtered retrieval first
            if use_concept_filter and concepts:
                primary_concept = self._select_primary_concept(concepts)
                
                if primary_concept:
                    logger.info(f"Retrieving with primary concept: {primary_concept}")
                    knowledge = retrieve_by_concept(
                        query=query,
                        concept_hint=primary_concept,
                        top_k=self.top_k
                    )
                    
                    # If concept-filtered retrieval returns results, use them
                    if knowledge:
                        return knowledge
            
            # Fall back to general semantic retrieval
            logger.info(f"Retrieving with general query: {query}")
            knowledge = retrieve(query=query, top_k=self.top_k)
            
            return knowledge
        
        except Exception as e:
            logger.error(f"Error during knowledge retrieval: {e}")
            return []
    
    def retrieve_with_scores(
        self, 
        concepts: List[str], 
        source_line: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve knowledge with similarity scores.
        
        Args:
            concepts: Extracted runtime concepts
            source_line: Executed source code line
        
        Returns:
            List of knowledge chunks with metadata
        """
        if not concepts and not source_line:
            return []
        
        try:
            query = self._build_query(concepts, source_line)
            
            # Use metadata retrieval for scoring
            results = retrieve_with_metadata(query=query, top_k=self.top_k)
            
            return results
        
        except Exception as e:
            logger.error(f"Error during retrieval with scores: {e}")
            return []
    
    def retrieve_batch(
        self, 
        steps_data: List[Dict[str, Any]]
    ) -> List[List[str]]:
        """
        Retrieve knowledge for multiple steps in batch.
        
        Args:
            steps_data: List of dicts with 'concepts' and 'source' keys
        
        Returns:
            List of knowledge chunk lists, one per step
        """
        all_knowledge = []
        
        for step_data in steps_data:
            concepts = step_data.get('concepts', [])
            source = step_data.get('source', '')
            
            knowledge = self.retrieve_for_step(concepts, source)
            all_knowledge.append(knowledge)
        
        logger.info(f"Retrieved knowledge for {len(all_knowledge)} steps")
        return all_knowledge


def retrieve_knowledge(concepts: List[str], source_line: str, top_k: int = 3) -> List[str]:
    """
    Convenience function for single-step knowledge retrieval.
    
    Args:
        concepts: Extracted concepts
        source_line: Source code line
        top_k: Number of chunks to retrieve
    
    Returns:
        List of relevant knowledge chunks
    """
    retriever = KnowledgeRetriever(top_k=top_k)
    return retriever.retrieve_for_step(concepts, source_line)
