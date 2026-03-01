"""
Step Explanation Engine - CLEAN VERSION

Generates clean, concise natural language explanations.
NO MARKDOWN formatting in output.
Explanations tailored to difficulty level.
"""

import logging
import re
from typing import List, Dict, Any
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trace_analysis.trace_processor import TraceProcessor
from trace_analysis.state_diff import StateDiffEngine, StateDiff
from execution.concept_extractor import ConceptExtractor
from execution.knowledge_retrieval import KnowledgeRetriever

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StepExplainer:
    """Generates clean, concise natural language explanations for execution steps."""
    
    def __init__(self, top_k_knowledge: int = 2, level: str = "medium"):
        """
        Initialize step explainer.
        
        Args:
            top_k_knowledge: Number of knowledge chunks (keep low for cleaner output)
            level: 'beginner', 'medium', or 'interview_ready'
        """
        self.trace_processor = TraceProcessor("")
        self.diff_engine = StateDiffEngine()
        self.concept_extractor = ConceptExtractor()
        self.knowledge_retriever = KnowledgeRetriever(top_k=top_k_knowledge)
        self.level = level.lower()
        
        logger.info(f"Initialized StepExplainer at '{self.level}' level")
    
    def _clean_markdown(self, text: str) -> str:
        """Remove ALL markdown formatting."""
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        # Remove inline code
        text = re.sub(r'`([^`]+)`', r'\1', text)
        # Remove bold/italic
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'__([^_]+)__', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)
        # Remove headers
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        # Remove bullets/lists
        text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
        # Clean whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _format_value(self, value: Any) -> str:
        """Format value without markdown."""
        if value is None:
            return "None"
        elif isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, (list, tuple)):
            if len(value) > 5:
                return f"{type(value).__name__} with {len(value)} items"
            return str(value)
        elif isinstance(value, dict):
            if len(value) > 3:
                return f"dict with {len(value)} keys"
            return str(value)
        else:
            return str(value)
    
    def _extract_core_concept(self, knowledge: List[str], level: str) -> str:
        """
        Extract ONE core concept sentence from knowledge.
        Clean, concise, no markdown.
        """
        if not knowledge:
            return ""
        
        # Clean first chunk
        text = self._clean_markdown(knowledge[0])
        
        # Split into sentences
        sentences = [s.strip() + '.' for s in text.split('. ') if s.strip()]
        
        if not sentences:
            return ""
        
        if level == "beginner":
            # Find simplest explanatory sentence
            for sent in sentences[:3]:
                words = sent.lower()
                if any(w in words for w in ['allows', 'helps', 'used for', 'means', 'enables']):
                    return sent
            return sentences[0]
        
        elif level == "medium":
            # First clear sentence
            return sentences[0]
        
        else:  # interview_ready
            # Find technical sentence
            for sent in sentences[:2]:
                words = sent.lower()
                if any(w in words for w in ['complexity', 'time', 'space', 'algorithm', 'optimize', 'performance']):
                    return sent
            return sentences[0]
    
    def _generate_explanation(
        self,
        step: Dict[str, Any],
        diff: StateDiff,
        concepts: List[str],
        knowledge: List[str],
        level: str
    ) -> str:
        """
        Generate CLEAN, CONCISE explanation.
        No markdown. To the point. Level-appropriate.
        """
        parts = []
        
        # Part 1: What happened (always brief)
        if diff.has_changes():
            # Created variables
            if diff.created and len(diff.created) == 1:
                change = diff.created[0]
                val = self._format_value(change.new_value)
                
                if level == "beginner":
                    parts.append(f"Variable {change.name} is created with value {val}.")
                elif level == "medium":
                    parts.append(f"{change.name} = {val}")
                else:  # interview_ready
                    parts.append(f"{change.name} initialized to {val}")
            
            elif diff.created and len(diff.created) > 1:
                names = ', '.join([c.name for c in diff.created])
                if level == "beginner":
                    parts.append(f"Variables {names} are created.")
                else:
                    parts.append(f"Created: {names}")
            
            # Modified variables
            if diff.modified:
                for change in diff.modified[:2]:  # Max 2 to keep concise
                    old = self._format_value(change.old_value)
                    new = self._format_value(change.new_value)
                    
                    if level == "beginner":
                        parts.append(f"{change.name} changes from {old} to {new}.")
                    elif level == "medium":
                        parts.append(f"{change.name}: {old} → {new}")
                    else:  # interview_ready
                        parts.append(f"{change.name} = {new}")
        
        # Part 2: Why it happened (only if we have good knowledge)
        if knowledge and len(parts) > 0:
            concept = self._extract_core_concept(knowledge, level)
            if concept and len(concept) < 100:  # Keep it short
                if level == "beginner":
                    parts.append(f"This happens because {concept.lower()}")
                else:
                    parts.append(concept)
        
        # Combine
        if not parts:
            # Fallback for steps with no changes
            line = step.get('line', 0)
            if level == "beginner":
                return f"Line {line} executes."
            elif level == "medium":
                return f"Executing line {line}"
            else:
                return f"L{line}"
        
        return ' '.join(parts)
    
    def generate_step_explanations(
        self,
        code: str,
        trace: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Main entry point.
        Returns clean, concise explanations for each step.
        """
        if not trace:
            return []
        
        # Process trace
        self.trace_processor = TraceProcessor(code)
        processed = self.trace_processor.process_trace(trace)
        
        # Compute diffs
        diffs = self.diff_engine.compute_trace_diffs(processed)
        
        # Extract concepts
        concepts_list = self.concept_extractor.extract_trace_concepts(processed, diffs)
        
        # Generate explanations
        enriched = []
        
        for i, (step, diff, concepts) in enumerate(zip(processed, diffs, concepts_list)):
            # Retrieve knowledge (only if step has meaningful changes)
            knowledge = []
            if diff.has_changes() and concepts:
                source = step.get('source', '')
                knowledge = self.knowledge_retriever.retrieve_for_step(concepts, source)
            
            # Generate clean explanation
            explanation = self._generate_explanation(
                step, diff, concepts, knowledge, self.level
            )
            
            enriched.append({
                'step': step.get('step'),
                'line': step.get('line'),
                'variables': step.get('variables', {}),
                'explanation': explanation  # CLEAN, NO MARKDOWN
            })
        
        logger.info(f"Generated {len(enriched)} clean explanations")
        return enriched