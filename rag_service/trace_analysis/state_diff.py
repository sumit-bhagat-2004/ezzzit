"""
State Difference Engine

Detects variable evolution between trace steps.
Identifies what changed, what was created, and what was removed.

Input: Two consecutive variable states
Output: Structured diff describing changes
"""

import logging
from typing import Dict, Any, List, Set

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VariableChange:
    """Represents a single variable change."""
    
    def __init__(self, name: str, change_type: str, old_value: Any = None, new_value: Any = None):
        """
        Initialize variable change.
        
        Args:
            name: Variable name
            change_type: Type of change ('created', 'modified', 'removed')
            old_value: Previous value (for modified/removed)
            new_value: New value (for created/modified)
        """
        self.name = name
        self.change_type = change_type
        self.old_value = old_value
        self.new_value = new_value
    
    def __repr__(self):
        if self.change_type == 'created':
            return f"{self.name} created = {self.new_value}"
        elif self.change_type == 'modified':
            return f"{self.name} changed: {self.old_value} → {self.new_value}"
        elif self.change_type == 'removed':
            return f"{self.name} removed (was {self.old_value})"
        return f"{self.name} {self.change_type}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'name': self.name,
            'type': self.change_type,
            'old_value': self.old_value,
            'new_value': self.new_value
        }


class StateDiff:
    """Represents the complete state difference between two steps."""
    
    def __init__(self):
        self.created: List[VariableChange] = []
        self.modified: List[VariableChange] = []
        self.removed: List[VariableChange] = []
    
    def has_changes(self) -> bool:
        """Check if there are any changes."""
        return bool(self.created or self.modified or self.removed)
    
    def get_all_changes(self) -> List[VariableChange]:
        """Get all changes as a single list."""
        return self.created + self.modified + self.removed
    
    def to_dict(self) -> Dict[str, List[Dict[str, Any]]]:
        """Convert to dictionary representation."""
        return {
            'created': [c.to_dict() for c in self.created],
            'modified': [c.to_dict() for c in self.modified],
            'removed': [c.to_dict() for c in self.removed]
        }
    
    def __repr__(self):
        changes = []
        for c in self.created:
            changes.append(str(c))
        for m in self.modified:
            changes.append(str(m))
        for r in self.removed:
            changes.append(str(r))
        return '; '.join(changes) if changes else 'No changes'


class StateDiffEngine:
    """Computes variable state differences between execution steps."""
    
    def __init__(self):
        """Initialize the state diff engine."""
        logger.info("Initialized StateDiffEngine")
    
    def _normalize_value(self, value: Any) -> Any:
        """
        Normalize variable values for comparison.
        
        Handles type conversion and string representation.
        
        Args:
            value: Variable value
        
        Returns:
            Normalized value
        """
        # Handle None
        if value is None:
            return None
        
        # Handle strings
        if isinstance(value, str):
            return value
        
        # Handle numbers
        if isinstance(value, (int, float)):
            return value
        
        # Handle booleans
        if isinstance(value, bool):
            return value
        
        # Handle lists/tuples
        if isinstance(value, (list, tuple)):
            return list(value)
        
        # Handle dicts
        if isinstance(value, dict):
            return value
        
        # Default: convert to string
        return str(value)
    
    def compute_diff(self, prev_vars: Dict[str, Any], curr_vars: Dict[str, Any]) -> StateDiff:
        """
        Compute the difference between two variable states.
        
        Args:
            prev_vars: Previous variable state (can be None for first step)
            curr_vars: Current variable state
        
        Returns:
            StateDiff object describing all changes
        """
        diff = StateDiff()
        
        # Handle first step (no previous state)
        if prev_vars is None or prev_vars == {}:
            for name, value in curr_vars.items():
                normalized_value = self._normalize_value(value)
                diff.created.append(VariableChange(name, 'created', new_value=normalized_value))
            return diff
        
        # Get all variable names from both states
        prev_names: Set[str] = set(prev_vars.keys())
        curr_names: Set[str] = set(curr_vars.keys())
        
        # Find created variables (in current but not in previous)
        created_names = curr_names - prev_names
        for name in created_names:
            value = self._normalize_value(curr_vars[name])
            diff.created.append(VariableChange(name, 'created', new_value=value))
        
        # Find removed variables (in previous but not in current)
        removed_names = prev_names - curr_names
        for name in removed_names:
            value = self._normalize_value(prev_vars[name])
            diff.removed.append(VariableChange(name, 'removed', old_value=value))
        
        # Find modified variables (in both but with different values)
        common_names = prev_names & curr_names
        for name in common_names:
            old_value = self._normalize_value(prev_vars[name])
            new_value = self._normalize_value(curr_vars[name])
            
            # Check if value actually changed
            if old_value != new_value:
                diff.modified.append(VariableChange(name, 'modified', old_value=old_value, new_value=new_value))
        
        logger.debug(f"Computed diff: {len(diff.created)} created, {len(diff.modified)} modified, {len(diff.removed)} removed")
        return diff
    
    def compute_trace_diffs(self, trace: List[Dict[str, Any]]) -> List[StateDiff]:
        """
        Compute state diffs for an entire trace.
        
        Args:
            trace: List of processed trace steps (each with 'variables' dict)
        
        Returns:
            List of StateDiff objects, one per trace step
        """
        if not trace:
            return []
        
        diffs = []
        prev_vars = None
        
        for i, step in enumerate(trace):
            curr_vars = step.get('variables', {})
            diff = self.compute_diff(prev_vars, curr_vars)
            diffs.append(diff)
            prev_vars = curr_vars
        
        logger.info(f"Computed {len(diffs)} state diffs for trace")
        return diffs


def compute_variable_diff(prev_vars: Dict[str, Any], curr_vars: Dict[str, Any]) -> StateDiff:
    """
    Convenience function to compute a single state diff.
    
    Args:
        prev_vars: Previous variable state
        curr_vars: Current variable state
    
    Returns:
        StateDiff object
    """
    engine = StateDiffEngine()
    return engine.compute_diff(prev_vars, curr_vars)
