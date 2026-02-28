"""
Example demonstrating different explanation levels.

Run this after starting the RAG service to see how explanations differ by level.
"""

import httpx
import asyncio
import json


SIMPLE_CODE = """a = 5
b = 3
sum_val = a + b
print(sum_val)"""


async def test_levels():
    """Test all three explanation levels."""
    
    levels = ["beginner", "medium", "interview_ready"]
    
    # Note: Update this URL to match your execution API
    rag_url = "http://localhost:8001/rag/explain_trace"
    
    for level in levels:
        print(f"\n{'='*60}")
        print(f"TESTING LEVEL: {level.upper()}")
        print(f"{'='*60}\n")
        
        payload = {
            "code": SIMPLE_CODE,
            "language": "python",
            "stdin": "",
            "level": level
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(rag_url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"Output: {data.get('output', '')}")
                print(f"\nExplanations ({len(data.get('trace', []))} steps):\n")
                
                for step in data.get('trace', []):
                    print(f"Step {step['step']}: {step['explanation']}")
                    print()
            else:
                print(f"Error: {response.status_code}")
                print(response.text)
        
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    print("Testing Trace Explanation Service with Different Levels")
    print("=" * 60)
    asyncio.run(test_levels())
