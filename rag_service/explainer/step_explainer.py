"""
Step Explanation Engine

Generates natural language explanations for each trace step.
Combines runtime context, state changes, and retrieved knowledge.

Main function: generate_step_explanations(code, trace)

Process per step:
1. Identify executed line
2. Compute state change
3. Extract runtime concept
4. Retrieve Snowflake knowledge
5. Generate grounded explanation
"""

import logging
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trace_analysis.trace_processor import TraceProcessor
from trace_analysis.state_diff import StateDiffEngine, StateDiff, VariableChange
from execution.concept_extractor import ConceptExtractor
from execution.knowledge_retrieval import KnowledgeRetriever

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StepExplainer:
    """Generates natural language explanations for execution steps."""
    
    def __init__(self, top_k_knowledge: int = 3, level: str = "medium"):
        """
        Initialize step explainer with all required components.
        
        Args:
            top_k_knowledge: Number of knowledge chunks to retrieve per step
            level: Explanation complexity level ('beginner', 'medium', 'interview_ready')
        """
        self.trace_processor = TraceProcessor("")  # Will be set later
        self.diff_engine = StateDiffEngine()
        self.concept_extractor = ConceptExtractor()
        self.knowledge_retriever = KnowledgeRetriever(top_k=top_k_knowledge)
        self.level = level.lower()
        
        logger.info(f"Initialized StepExplainer at '{self.level}' level")
    
    def _format_variable_changes(self, diff: StateDiff, level: str = None) -> str:
        """
        Format variable changes into natural language based on complexity level.
        
        Args:
            diff: State difference
            level: Complexity level (uses self.level if not provided)
        
        Returns:
            Formatted change description
        """
        if level is None:
            level = self.level
            
        parts = []
        
        # Created variables
        for change in diff.created:
            value_str = self._format_value(change.new_value)
            
            if level == "beginner":
                parts.append(f"A new variable `{change.name}` is created and stores the value {value_str}.")
            elif level == "medium":
                parts.append(f"Variable `{change.name}` is created with value {value_str}.")
            else:  # interview_ready
                parts.append(f"`{change.name}` initialized: {value_str}.")
        
        # Modified variables
        for change in diff.modified:
            old_str = self._format_value(change.old_value)
            new_str = self._format_value(change.new_value)
            
            if level == "beginner":
                parts.append(f"Variable `{change.name}` changes from {old_str} to {new_str}.")
            elif level == "medium":
                parts.append(f"`{change.name}` updated: {old_str} → {new_str}.")
            else:  # interview_ready
                parts.append(f"`{change.name}`: {old_str} → {new_str} (mutation).")
        
        # Removed variables (rare, usually scope-related)
        for change in diff.removed:
            if level == "beginner":
                parts.append(f"Variable `{change.name}` is no longer available (went out of scope).")
            elif level == "medium":
                parts.append(f"`{change.name}` goes out of scope.")
            else:  # interview_ready
                parts.append(f"`{change.name}` deallocated (scope exit).")
        
        return ' '.join(parts) if parts else ""
    
    def _format_value(self, value: Any) -> str:
        """
        Format a value for display in explanation.
        
        Args:
            value: Variable value
        
        Returns:
            Formatted string representation
        """
        if value is None:
            return "`None`"
        elif isinstance(value, str):
            return f'`"{value}"`'
        elif isinstance(value, (list, tuple)):
            if len(value) > 5:
                return f"`{type(value).__name__}` with {len(value)} elements"
            return f"`{value}`"
        elif isinstance(value, dict):
            if len(value) > 3:
                return f"`dict` with {len(value)} keys"
            return f"`{value}`"
        else:
            return f"`{value}`"
    
    def _extract_key_insight(self, knowledge_chunks: List[str], level: str = None) -> str:
        """
        Extract the most relevant insight from retrieved knowledge based on level.
        
        Args:
            knowledge_chunks: List of knowledge strings
            level: Complexity level (uses self.level if not provided)
        
        Returns:
            Key insight sentence
        """
        if level is None:
            level = self.level
            
        if not knowledge_chunks:
            return ""
        
        # Use the first (most relevant) chunk
        first_chunk = knowledge_chunks[0]
        
        # Split into sentences
        sentences = first_chunk.split('. ')
        
        # For beginner, use more sentences; for interview_ready, use fewer
        if level == "beginner":
            num_sentences = 2
        elif level == "medium":
            num_sentences = 1
        else:  # interview_ready
            # For interview_ready, extract most technical sentence
            num_sentences = 1
        
        # Take sentences
        if sentences:
            selected_sentences = sentences[:num_sentences]
            key_sentence = '. '.join(s.strip() for s in selected_sentences if s.strip())
            if key_sentence and not key_sentence.endswith('.'):
                key_sentence += '.'
            return key_sentence
        
        return ""
    
    def _generate_base_explanation(self, step: Dict[str, Any], diff: StateDiff, level: str = None) -> str:
        """
        Generate base explanation from step and state diff based on complexity level.
        
        Args:
            step: Trace step
            diff: State difference
            level: Complexity level (uses self.level if not provided)
        
        Returns:
            Base explanation string
        """
        if level is None:
            level = self.level
            
        source = step.get('source', '')
        line_num = step.get('line', 0)
        
        # Special case: first step
        if step.get('step') == 1 and not diff.has_changes():
            if level == "beginner":
                return "The program starts executing."
            elif level == "medium":
                return "Program execution begins."
            else:  # interview_ready
                return "Execution context initialized."
        
        # Build explanation
        parts = []
        
        # Describe the line being executed
        if source:
            if level == "beginner":
                parts.append(f"Line {line_num} runs: `{source}`.")
            elif level == "medium":
                parts.append(f"Executing line {line_num}: `{source}`.")
            else:  # interview_ready
                parts.append(f"L{line_num}: `{source}`.")
        
        # Describe variable changes
        if diff.has_changes():
            change_desc = self._format_variable_changes(diff, level)
            if change_desc:
                parts.append(change_desc)
        
        return ' '.join(parts) if parts else f"Executing line {line_num}."
    
    def _generate_explanation(
        self, 
        step: Dict[str, Any], 
        diff: StateDiff,
        concepts: List[str],
        knowledge: List[str],
        level: str = None
    ) -> str:
        """
        Generate complete explanation with knowledge grounding based on level.
        
        Args:
            step: Trace step
            diff: State difference
            concepts: Extracted concepts
            knowledge: Retrieved knowledge chunks
            level: Complexity level (uses self.level if not provided)
        
        Returns:
            Complete natural language explanation
        """
        if level is None:
            level = self.level
            
        # Start with base explanation (what happened)
        base = self._generate_base_explanation(step, diff, level)
        
        # Add knowledge-grounded insight (why it happened)
        insight = self._extract_key_insight(knowledge, level)
        
        # Combine base and insight based on level
        if insight:
            if level == "beginner":
                # More explicit connection for beginners
                if base.endswith('.'):
                    explanation = f"{base} This happens because {insight.lower() if insight else insight}"
                else:
                    explanation = f"{base}. This happens because {insight.lower() if insight else insight}"
            elif level == "medium":
                # Standard combination
                if base.endswith('.'):
                    explanation = f"{base} {insight}"
                else:
                    explanation = f"{base}. {insight}"
            else:  # interview_ready
                # More concise, technical
                if base.endswith('.'):
                    explanation = f"{base} {insight}"
                else:
                    explanation = f"{base}. {insight}"
        else:
            explanation = base
        
        logger.debug(f"Generated explanation for step {step.get('step')}: {explanation[:50]}...")
        return explanation
    
    def generate_step_explanations(self, code: str, trace: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate explanations for all steps in a trace.
        
        Main entry point for explanation generation.
        
        Args:
            code: Source code string
            trace: Raw or processed trace from execution API
        
        Returns:
            List of enriched steps with explanations
        """
        if not trace:
            logger.warning("Empty trace provided")
            return []
        
        # Initialize trace processor with code
        self.trace_processor = TraceProcessor(code)
        
        # Step 1: Process trace (clean and order)
        processed_trace = self.trace_processor.process_trace(trace)
        logger.info(f"Processed {len(processed_trace)} trace steps")
        
        # Step 2: Compute state diffs
        diffs = self.diff_engine.compute_trace_diffs(processed_trace)
        logger.info(f"Computed {len(diffs)} state diffs")
        
        # Step 3: Extract concepts
        concepts_per_step = self.concept_extractor.extract_trace_concepts(processed_trace, diffs)
        logger.info(f"Extracted concepts for {len(concepts_per_step)} steps")
        
        # Step 4 & 5: Retrieve knowledge and generate explanations
        enriched_steps = []
        prev_step = None
        
        for i, (step, diff, concepts) in enumerate(zip(processed_trace, diffs, concepts_per_step)):
            # Retrieve relevant knowledge
            source = step.get('source', '')
            knowledge = self.knowledge_retriever.retrieve_for_step(concepts, source)
            
            # Generate explanation with level awareness
            explanation = self._generate_explanation(step, diff, concepts, knowledge, self.level)
            
            # Build enriched step
            enriched_step = {
                'step': step.get('step'),
                'line': step.get('line'),
                'variables': step.get('variables', {}),
                'explanation': explanation
            }
            
            enriched_steps.append(enriched_step)
            prev_step = step
        
        logger.info(f"Generated explanations for {len(enriched_steps)} steps")
        return enriched_steps
    
    def generate_single_explanation(
        self, 
        step: Dict[str, Any],
        prev_variables: Dict[str, Any],
        source_code: str
    ) -> str:
        """
        Generate explanation for a single step (convenience method).
        
        Args:
            step: Trace step
            prev_variables: Variables from previous step
            source_code: Full source code
        
        Returns:
            Explanation string
        """
        # Compute diff
        curr_variables = step.get('variables', {})
        diff = self.diff_engine.compute_diff(prev_variables, curr_variables)
        
        # Extract concepts
        concepts = self.concept_extractor.extract_concepts(step, diff)
        
        # Retrieve knowledge
        source_line = step.get('source', '')
        knowledge = self.knowledge_retriever.retrieve_for_step(concepts, source_line)
        
        # Generate explanation
        explanation = self._generate_explanation(step, diff, concepts, knowledge)
        
        return explanation


def generate_explanations(code: str, trace: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convenience function to generate explanations for a full trace.
    
    Args:
        code: Source code string
        trace: Execution trace
    
    Returns:
        Enriched trace with explanations
    """
    explainer = StepExplainer()
    return explainer.generate_step_explanations(code, trace)
