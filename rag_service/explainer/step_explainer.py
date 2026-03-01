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
    """Generates clean, technical natural language explanations for execution steps."""
    
    def __init__(self, top_k_knowledge: int = None, level: str = "medium"):
        """
        Initialize step explainer.
        
        Args:
            top_k_knowledge: Number of knowledge chunks (auto-adjusted per level if None)
            level: 'beginner', 'medium', or 'interview_ready'
        """
        self.trace_processor = TraceProcessor("")
        self.diff_engine = StateDiffEngine()
        self.concept_extractor = ConceptExtractor()
        self.level = level.lower()
        
        # Auto-adjust knowledge retrieval based on level
        if top_k_knowledge is None:
            if self.level == "beginner":
                top_k_knowledge = 3  # More context for detailed explanations
            elif self.level == "medium":
                top_k_knowledge = 2  # Balanced
            else:  # interview_ready
                top_k_knowledge = 2  # Focused technical content
        
        self.knowledge_retriever = KnowledgeRetriever(top_k=top_k_knowledge)
        
        logger.info(f"Initialized StepExplainer at '{self.level}' level with top_k={top_k_knowledge}")
    
    def _clean_markdown(self, text: str) -> str:
        """Remove ALL markdown formatting and clean up text."""
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        # Remove inline code
        text = re.sub(r'`([^`]+)`', r'\1', text)
        # Remove bold/italic
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'__([^_]+)__', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)
        # Remove headers (with proper spacing)
        text = re.sub(r'^#{1,6}\s+(.+)$', r'\1. ', text, flags=re.MULTILINE)
        # Remove bullets/lists
        text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
        # Clean multiple spaces
        text = re.sub(r'\s+', ' ', text)
        # Clean multiple periods
        text = re.sub(r'\.\s*\.+', '.', text)
        text = text.strip()
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
        Extract appropriate concept explanation based on level.
        Beginner: Multiple sentences, very explanatory
        Medium: 1-2 clear sentences with context
        Interview Ready: Technical sentences with implementation/complexity details
        """
        if not knowledge:
            return ""
        
        # Clean all chunks and combine
        cleaned_chunks = [self._clean_markdown(k) for k in knowledge[:2]]
        all_text = ' '.join(cleaned_chunks)
        
        # Split into clean sentences
        raw_sentences = [s.strip() for s in all_text.split('.') if s.strip() and len(s.strip()) > 15]
        sentences = [s + '.' for s in raw_sentences]
        
        if not sentences:
            return ""
        
        if level == "beginner":
            # Find 2-3 explanatory sentences for comprehensive understanding
            explanatory = []
            for sent in sentences[:6]:
                words = sent.lower()
                # Skip title-like sentences (too short or all caps feel)
                if len(sent) < 20:
                    continue
                # Look for beginner-friendly explanations
                if any(w in words for w in ['allows', 'helps', 'used for', 'means', 'enables', 'is a', 'are', 'can', 'provides', 'makes']):
                    explanatory.append(sent)
                if len(explanatory) >= 2:
                    break
            
            if explanatory:
                return ' '.join(explanatory)
            # Fallback: first 2 substantive sentences
            return ' '.join(sentences[:2])
        
        elif level == "medium":
            # 1-2 clear, balanced sentences with context
            result_sentences = []
            for sent in sentences[:4]:
                # Skip very short or title-like sentences
                if len(sent) < 25:
                    continue
                result_sentences.append(sent)
                if len(result_sentences) >= 2:
                    break
            
            if result_sentences:
                return ' '.join(result_sentences)
            return sentences[0] if sentences else ""
        
        else:  # interview_ready
            # Find technical sentences with implementation details and complexity
            technical = []
            for sent in sentences[:6]:
                words = sent.lower()
                # Skip title-like sentences
                if len(sent) < 25:
                    continue
                # Look for technical concepts
                if any(w in words for w in ['complexity', 'time', 'space', 'algorithm', 'optimize', 
                                           'performance', 'memory', 'o(', 'stack', 'heap', 'reference',
                                           'mutation', 'immutable', 'allocation', 'iteration', 'constant',
                                           'linear', 'evaluated', 'executes']):
                    technical.append(sent)
                if len(technical) >= 2:
                    break
            
            if technical:
                return ' '.join(technical)
            
            # Fallback: first substantive sentences
            substantive = [s for s in sentences[:3] if len(s) > 25]
            return ' '.join(substantive[:2]) if substantive else (sentences[0] if sentences else "")
    
    def _generate_explanation(
        self,
        step: Dict[str, Any],
        diff: StateDiff,
        concepts: List[str],
        knowledge: List[str],
        level: str
    ) -> str:
        """
        Generate level-appropriate explanation.
        Beginner: Longer, layman terms, very explanatory
        Medium: Balanced, clear
        Interview Ready: Technical with complexity details, concise but complete
        """
        parts = []
        source = step.get('source', '')
        line = step.get('line', 0)
        
        # BEGINNER LEVEL - Longer, more explanatory
        if level == "beginner":
            if diff.has_changes():
                # Created variables
                for change in diff.created:
                    val = self._format_value(change.new_value)
                    val_type = type(change.new_value).__name__
                    
                    parts.append(f"A new variable named {change.name} is created and stores the value {val}. This is a {val_type} type in Python.")
                
                # Modified variables
                for change in diff.modified:
                    old = self._format_value(change.old_value)
                    new = self._format_value(change.new_value)
                    
                    parts.append(f"The variable {change.name} changes its value from {old} to {new}. The old value is replaced with the new value in memory.")
            
            # Add context from source
            if source and not parts:
                parts.append(f"Line {line} executes the code: {source}. This line runs but doesn't create or change any variables yet.")
            
            # Add detailed knowledge explanation
            if knowledge:
                concept = self._extract_core_concept(knowledge, level)
                if concept:
                    parts.append(concept)
            
            # Make it even more explanatory if too short
            if len(' '.join(parts)) < 80 and diff.has_changes():
                if diff.created:
                    parts.append("Variables are like containers that hold values in your program so you can use them later.")
        
        # MEDIUM LEVEL - Balanced with context
        elif level == "medium":
            if diff.has_changes():
                # Created variables
                if diff.created and len(diff.created) == 1:
                    change = diff.created[0]
                    val = self._format_value(change.new_value)
                    val_type = type(change.new_value).__name__
                    parts.append(f"Variable {change.name} is assigned the value {val} ({val_type}).")
                elif diff.created:
                    for change in diff.created[:2]:
                        val = self._format_value(change.new_value)
                        parts.append(f"{change.name} = {val}.")
                
                # Modified variables
                for change in diff.modified[:2]:
                    old = self._format_value(change.old_value)
                    new = self._format_value(change.new_value)
                    parts.append(f"{change.name} updated from {old} to {new}.")
            
            # Always add knowledge context for medium level
            if knowledge:
                concept = self._extract_core_concept(knowledge, level)
                if concept:
                    parts.append(concept)
        
        # INTERVIEW READY - Technical with substantial details
        else:  # interview_ready
            if diff.has_changes():
                # Created variables with technical details
                for change in diff.created:
                    val = self._format_value(change.new_value)
                    val_type = type(change.new_value).__name__
                    
                    # Add technical context with more detail
                    if isinstance(change.new_value, list):
                        size = len(change.new_value)
                        parts.append(f"{change.name} initialized as empty list (dynamic array, O(1) append amortized, O(n) access by index).")
                    elif isinstance(change.new_value, dict):
                        parts.append(f"{change.name} initialized as dictionary (hash table implementation, O(1) average case insertion/lookup, O(n) worst case).")
                    elif isinstance(change.new_value, (int, float)):
                        parts.append(f"{change.name} = {val} (primitive immutable type, stored by value, assignment is O(1)).")
                    elif isinstance(change.new_value, str):
                        parts.append(f"{change.name} = {val} (immutable string, stored as character array, concatenation creates new object).")
                    else:
                        parts.append(f"{change.name} = {val} (type: {val_type}).")
                
                # Modified variables with mutation context
                for change in diff.modified:
                    old = self._format_value(change.old_value)
                    new = self._format_value(change.new_value)
                    
                    # Check if it's a mutating operation
                    if isinstance(change.new_value, list) and isinstance(change.old_value, list):
                        size_change = len(change.new_value) - len(change.old_value)
                        if size_change > 0:
                            parts.append(f"{change.name} modified: {old} → {new}. List grew by {size_change} element(s) via in-place mutation (O(1) amortized append, potential array resize).")
                        elif size_change < 0:
                            parts.append(f"{change.name} modified: {old} → {new}. List reduced by {abs(size_change)} element(s) (O(n) for removal from middle, O(1) for pop).")
                        else:
                            parts.append(f"{change.name} modified: {old} → {new}. List mutated in place (element update is O(1)).")
                    elif isinstance(change.new_value, dict) and isinstance(change.old_value, dict):
                        parts.append(f"{change.name} modified: {old} → {new}. Dictionary mutated (hash table update is O(1) average case).")
                    else:
                        parts.append(f"{change.name} reassigned: {old} → {new}. Variable rebinding creates new reference, old object may be garbage collected.")
            
            # Always add technical knowledge for interview level
            if knowledge:
                concept = self._extract_core_concept(knowledge, level)
                if concept:
                    parts.append(concept)
        
        # Combine
        if not parts:
            # Fallback for steps with no changes
            if level == "beginner":
                return f"Line {line} executes. This line is running as part of the program flow."
            elif level == "medium":
                return f"Executing line {line}"
            else:
                return f"L{line}: {source if source else 'execution'}"
        
        return ' '.join(parts)
    
    def generate_step_explanations(
        self,
        code: str,
        trace: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Main entry point.
        Returns clean, technical explanations for each step.
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