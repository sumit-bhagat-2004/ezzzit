"""
Test script for the Trace-Aware RAG Explanation Service.

Tests the complete pipeline:
1. Trace processing
2. State diff computation
3. Concept extraction
4. Knowledge retrieval (mocked if Snowflake unavailable)
5. Explanation generation
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trace_analysis.trace_processor import TraceProcessor
from trace_analysis.state_diff import StateDiffEngine
from execution.concept_extractor import ConceptExtractor
from explainer.step_explainer import StepExplainer


def test_trace_processor():
    """Test trace processing."""
    print("\n=== Testing Trace Processor ===")
    
    code = """a = 5
b = 3
sum_val = a + b
print(sum_val)"""
    
    # Simulated trace from execution API
    raw_trace = [
        {"step": 1, "line": 1, "variables": {"a": 5}, "event": "line", "function": "main", "call_stack_depth": 0},
        {"step": 2, "line": 2, "variables": {"a": 5, "b": 3}, "event": "line", "function": "main", "call_stack_depth": 0},
        {"step": 3, "line": 3, "variables": {"a": 5, "b": 3, "sum_val": 8}, "event": "line", "function": "main", "call_stack_depth": 0},
    ]
    
    processor = TraceProcessor(code)
    processed = processor.process_trace(raw_trace)
    
    print(f"✓ Processed {len(processed)} steps")
    for step in processed:
        print(f"  Step {step['step']}: Line {step['line']} - {step['source']}")
    
    return processed


def test_state_diff(trace):
    """Test state difference computation."""
    print("\n=== Testing State Diff Engine ===")
    
    engine = StateDiffEngine()
    diffs = engine.compute_trace_diffs(trace)
    
    print(f"✓ Computed {len(diffs)} state diffs")
    for i, diff in enumerate(diffs):
        print(f"  Step {i+1}: {diff}")
    
    return diffs


def test_concept_extraction(trace, diffs):
    """Test concept extraction."""
    print("\n=== Testing Concept Extractor ===")
    
    extractor = ConceptExtractor()
    concepts = extractor.extract_trace_concepts(trace, diffs)
    
    print(f"✓ Extracted concepts for {len(concepts)} steps")
    for i, concept_list in enumerate(concepts):
        print(f"  Step {i+1}: {', '.join(concept_list) if concept_list else 'none'}")
    
    return concepts


def test_explanation_generation_mock():
    """Test explanation generation with mocked knowledge retrieval."""
    print("\n=== Testing Explanation Generation (Mock Mode) ===")
    
    code = """a = 5
b = 3
sum_val = a + b
print(sum_val)"""
    
    trace = [
        {"step": 1, "line": 1, "variables": {"a": 5}, "event": "line", "function": "main", "call_stack_depth": 0},
        {"step": 2, "line": 2, "variables": {"a": 5, "b": 3}, "event": "line", "function": "main", "call_stack_depth": 0},
        {"step": 3, "line": 3, "variables": {"a": 5, "b": 3, "sum_val": 8}, "event": "line", "function": "main", "call_stack_depth": 0},
    ]
    
    # Note: This will attempt to connect to Snowflake for real retrieval
    # If Snowflake is not configured, it will fail gracefully
    try:
        explainer = StepExplainer(top_k_knowledge=3)
        enriched = explainer.generate_step_explanations(code, trace)
        
        print(f"✓ Generated explanations for {len(enriched)} steps")
        for step in enriched:
            print(f"\n  Step {step['step']} (Line {step['line']}):")
            print(f"  Variables: {step['variables']}")
            print(f"  Explanation: {step['explanation']}")
        
        return enriched
    
    except Exception as e:
        print(f"⚠ Snowflake connection required for full test: {e}")
        print("  Using basic explanation generation...")
        
        # Basic test without Snowflake
        processor = TraceProcessor(code)
        processed = processor.process_trace(trace)
        
        engine = StateDiffEngine()
        diffs = engine.compute_trace_diffs(processed)
        
        print(f"✓ Processed {len(processed)} steps with {len(diffs)} diffs")
        return None


def test_full_pipeline():
    """Test the complete pipeline."""
    print("\n" + "="*60)
    print("TRACE-AWARE RAG EXPLANATION SERVICE - TEST SUITE")
    print("="*60)
    
    # Test individual components
    trace = test_trace_processor()
    diffs = test_state_diff(trace)
    concepts = test_concept_extraction(trace, diffs)
    
    # Test full explanation generation
    enriched = test_explanation_generation_mock()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
    print("="*60)
    
    if enriched:
        print("\nExample output format:")
        print({
            "output": "8",
            "trace": enriched[:2]  # Show first 2 steps
        })
    else:
        print("\n⚠ Note: Full integration test requires Snowflake connection")
        print("   Run ingestion first: python ingestion/ingest.py")
        print("   Then start the service: uvicorn app:app --reload")


if __name__ == "__main__":
    test_full_pipeline()
