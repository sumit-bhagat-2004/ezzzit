"""
Runtime Concept Extractor

Extracts semantic programming concepts from execution context.
Maps runtime behavior to conceptual knowledge categories.

Rules:
- assignment → variable assignment
- arithmetic change → arithmetic operation
- if evaluation → conditional branching
- loop repetition → iteration
- function depth increase → function call
"""

import logging
import re
from typing import List, Dict, Any, Set
from trace_analysis.state_diff import StateDiff

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConceptExtractor:
    """Extracts semantic programming concepts from execution traces."""
    
    # Keyword patterns for concept detection
    CONTROL_FLOW_KEYWORDS = {
        'conditional': ['if', 'elif', 'else'],
        'loop': ['for', 'while', 'in'],
        'function': ['def', 'return'],
        'exception': ['try', 'except', 'finally', 'raise']
    }
    
    ARITHMETIC_OPERATORS = ['+', '-', '*', '/', '//', '%', '**']
    COMPARISON_OPERATORS = ['==', '!=', '<', '>', '<=', '>=']
    LOGICAL_OPERATORS = ['and', 'or', 'not']
    ASSIGNMENT_OPERATORS = ['=', '+=', '-=', '*=', '/=']
    
    def __init__(self):
        """Initialize concept extractor."""
        logger.info("Initialized ConceptExtractor")
    
    def _detect_from_source(self, source_line: str) -> Set[str]:
        """
        Detect concepts from source code line.
        
        Args:
            source_line: Line of source code
        
        Returns:
            Set of detected concepts
        """
        concepts = set()
        
        if not source_line:
            return concepts
        
        source_lower = source_line.lower().strip()
        
        # Check for control flow keywords
        for concept_type, keywords in self.CONTROL_FLOW_KEYWORDS.items():
            for keyword in keywords:
                # Use word boundaries to avoid false matches
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, source_lower):
                    if concept_type == 'conditional':
                        concepts.add('conditional')
                    elif concept_type == 'loop':
                        concepts.add('iteration')
                    elif concept_type == 'function':
                        concepts.add('function_call')
                    elif concept_type == 'exception':
                        concepts.add('exception_handling')
        
        # Check for arithmetic operations
        for op in self.ARITHMETIC_OPERATORS:
            if op in source_line:
                concepts.add('arithmetic')
                break
        
        # Check for comparison operations
        for op in self.COMPARISON_OPERATORS:
            if op in source_line:
                concepts.add('comparison')
                break
        
        # Check for logical operations
        for op in self.LOGICAL_OPERATORS:
            pattern = r'\b' + re.escape(op) + r'\b'
            if re.search(pattern, source_lower):
                concepts.add('logical_operation')
                break
        
        # Check for assignment
        if '=' in source_line and '==' not in source_line and '!=' not in source_line:
            concepts.add('assignment')
        
        # Check for list/array operations
        if '[' in source_line and ']' in source_line:
            concepts.add('indexing')
        
        # Check for function calls (pattern: word followed by parentheses)
        if re.search(r'\w+\s*\(', source_line):
            concepts.add('function_call')
        
        # Check for list comprehensions
        if re.search(r'\[.*for.*in.*\]', source_line):
            concepts.add('list_comprehension')
        
        # Check for dictionary operations
        if '{' in source_line and ':' in source_line and '}' in source_line:
            concepts.add('dictionary')
        
        # Check for string operations
        if re.search(r'["\'].*["\']', source_line):
            concepts.add('string')
        
        return concepts
    
    def _detect_from_state_diff(self, diff: StateDiff) -> Set[str]:
        """
        Detect concepts from variable state changes.
        
        Args:
            diff: State difference between steps
        
        Returns:
            Set of detected concepts
        """
        concepts = set()
        
        if not diff.has_changes():
            return concepts
        
        # Variable creation
        if diff.created:
            concepts.add('assignment')
            
            # Check types of created variables
            for change in diff.created:
                value = change.new_value
                if isinstance(value, list):
                    concepts.add('list')
                elif isinstance(value, dict):
                    concepts.add('dictionary')
                elif isinstance(value, (int, float)):
                    concepts.add('numeric')
                elif isinstance(value, str):
                    concepts.add('string')
        
        # Variable modification
        if diff.modified:
            concepts.add('mutation')
            
            # Check for arithmetic changes
            for change in diff.modified:
                old_val = change.old_value
                new_val = change.new_value
                
                # Numeric arithmetic
                if isinstance(old_val, (int, float)) and isinstance(new_val, (int, float)):
                    concepts.add('arithmetic')
                
                # List/collection modification
                if isinstance(old_val, list) and isinstance(new_val, list):
                    if len(new_val) > len(old_val):
                        concepts.add('list_append')
                    elif len(new_val) < len(old_val):
                        concepts.add('list_removal')
        
        # Variable removal (going out of scope)
        if diff.removed:
            concepts.add('scope')
        
        return concepts
    
    def _detect_from_event(self, event: str, prev_depth: int, curr_depth: int) -> Set[str]:
        """
        Detect concepts from trace event and call stack changes.
        
        Args:
            event: Trace event type ('line', 'call', 'return')
            prev_depth: Previous call stack depth
            curr_depth: Current call stack depth
        
        Returns:
            Set of detected concepts
        """
        concepts = set()
        
        # Function call detection
        if curr_depth > prev_depth:
            concepts.add('function_call')
        
        # Function return detection
        if curr_depth < prev_depth:
            concepts.add('function_return')
        
        # Event-based detection
        if event == 'call':
            concepts.add('function_call')
        elif event == 'return':
            concepts.add('function_return')
        
        return concepts
    
    def extract_concepts(
        self, 
        step: Dict[str, Any], 
        diff: StateDiff, 
        prev_step: Dict[str, Any] = None
    ) -> List[str]:
        """
        Extract all relevant concepts from a trace step.
        
        Combines information from:
        - Source code keywords
        - Variable state changes
        - Execution events
        
        Args:
            step: Current trace step
            diff: State difference for this step
            prev_step: Previous trace step (optional)
        
        Returns:
            List of extracted concept keywords
        """
        all_concepts = set()
        
        # Extract from source code
        source_line = step.get('source', '')
        source_concepts = self._detect_from_source(source_line)
        all_concepts.update(source_concepts)
        
        # Extract from state diff
        diff_concepts = self._detect_from_state_diff(diff)
        all_concepts.update(diff_concepts)
        
        # Extract from execution events
        event = step.get('event', 'line')
        curr_depth = step.get('call_stack_depth', 0)
        prev_depth = prev_step.get('call_stack_depth', 0) if prev_step else 0
        event_concepts = self._detect_from_event(event, prev_depth, curr_depth)
        all_concepts.update(event_concepts)
        
        # Convert to sorted list for consistency
        concept_list = sorted(list(all_concepts))
        
        logger.debug(f"Extracted concepts for line {step.get('line')}: {concept_list}")
        return concept_list
    
    def extract_trace_concepts(
        self, 
        trace: List[Dict[str, Any]], 
        diffs: List[StateDiff]
    ) -> List[List[str]]:
        """
        Extract concepts for an entire trace.
        
        Args:
            trace: List of trace steps
            diffs: List of state diffs (one per step)
        
        Returns:
            List of concept lists, one per trace step
        """
        if len(trace) != len(diffs):
            logger.warning(f"Trace length ({len(trace)}) != diffs length ({len(diffs)})")
            return []
        
        all_concepts = []
        prev_step = None
        
        for i, (step, diff) in enumerate(zip(trace, diffs)):
            concepts = self.extract_concepts(step, diff, prev_step)
            all_concepts.append(concepts)
            prev_step = step
        
        logger.info(f"Extracted concepts for {len(all_concepts)} trace steps")
        return all_concepts


def extract_step_concepts(step: Dict[str, Any], diff: StateDiff, prev_step: Dict[str, Any] = None) -> List[str]:
    """
    Convenience function to extract concepts from a single step.
    
    Args:
        step: Trace step
        diff: State diff
        prev_step: Previous step (optional)
    
    Returns:
        List of concept keywords
    """
    extractor = ConceptExtractor()
    return extractor.extract_concepts(step, diff, prev_step)
