"""
Trace Processor Module

Responsibilities:
- Preserve execution order
- Ignore duplicate interpreter frames
- Map line numbers to source code
- Prepare step context for explanation

Input: Raw trace from execution API
Output: Processed trace steps ready for explanation
"""

import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TraceProcessor:
    """Processes raw execution traces into structured step contexts."""
    
    def __init__(self, code: str):
        """
        Initialize trace processor with source code.
        
        Args:
            code: Source code string
        """
        self.code = code
        self.code_lines = code.split('\n')
        logger.info(f"Initialized TraceProcessor with {len(self.code_lines)} lines of code")
    
    def get_line_content(self, line_num: int) -> str:
        """
        Get the source code content for a given line number.
        
        Args:
            line_num: 1-indexed line number
        
        Returns:
            Source code line content, or empty string if out of bounds
        """
        if 0 < line_num <= len(self.code_lines):
            return self.code_lines[line_num - 1].strip()
        return ""
    
    def is_redundant_frame(self, step: Dict[str, Any], prev_step: Dict[str, Any] = None) -> bool:
        """
        Determine if a trace step is a redundant interpreter frame.
        
        Redundant frames include:
        - Multiple consecutive steps on the same line with no variable changes
        - Internal interpreter events (e.g., 'call' events for built-in functions)
        
        Args:
            step: Current trace step
            prev_step: Previous trace step (if any)
        
        Returns:
            True if step is redundant and should be filtered out
        """
        if prev_step is None:
            return False
        
        # Check if same line with identical variables
        same_line = step.get('line') == prev_step.get('line')
        same_vars = step.get('variables') == prev_step.get('variables')
        
        if same_line and same_vars:
            logger.debug(f"Filtering redundant frame at line {step.get('line')}")
            return True
        
        return False
    
    def process_trace(self, raw_trace: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process raw trace into clean, ordered steps.
        
        Filters out redundant frames while preserving execution order.
        Enriches each step with source code context.
        
        Args:
            raw_trace: Raw trace from execution API
        
        Returns:
            List of processed trace steps with context
        """
        if not raw_trace:
            logger.warning("Empty trace provided")
            return []
        
        processed_steps = []
        prev_step = None
        
        for i, step in enumerate(raw_trace):
            # Skip redundant frames
            if self.is_redundant_frame(step, prev_step):
                continue
            
            # Enrich step with source code context
            line_num = step.get('line', 0)
            source_line = self.get_line_content(line_num)
            
            enriched_step = {
                'step': len(processed_steps) + 1,  # Re-index after filtering
                'line': line_num,
                'source': source_line,
                'function': step.get('function', 'main'),
                'variables': step.get('variables', {}),
                'event': step.get('event', 'line'),
                'call_stack_depth': step.get('call_stack_depth', 0)
            }
            
            processed_steps.append(enriched_step)
            prev_step = step
        
        logger.info(f"Processed {len(raw_trace)} raw steps into {len(processed_steps)} clean steps")
        return processed_steps
    
    def get_execution_context(self, step: Dict[str, Any], window: int = 2) -> Dict[str, Any]:
        """
        Get contextual information around a trace step.
        
        Provides surrounding source lines for better understanding.
        
        Args:
            step: Trace step
            window: Number of lines before/after to include
        
        Returns:
            Dictionary with contextual information
        """
        line_num = step.get('line', 0)
        
        # Get surrounding lines
        start_line = max(1, line_num - window)
        end_line = min(len(self.code_lines), line_num + window)
        
        context_lines = []
        for i in range(start_line, end_line + 1):
            context_lines.append({
                'line_num': i,
                'content': self.get_line_content(i),
                'is_current': i == line_num
            })
        
        return {
            'current_line': line_num,
            'current_source': step.get('source', ''),
            'context_window': context_lines,
            'function': step.get('function', 'main'),
            'depth': step.get('call_stack_depth', 0)
        }


def process_execution_trace(code: str, trace: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convenience function to process a trace with source code.
    
    Args:
        code: Source code string
        trace: Raw trace from execution API
    
    Returns:
        Processed trace steps
    """
    processor = TraceProcessor(code)
    return processor.process_trace(trace)
