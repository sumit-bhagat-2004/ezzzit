import os
import json
from google import genai
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY not found. AI features will be disabled.")
            self.client = None
            return
        
        self.client = genai.Client(api_key=api_key)
    
    def analyze_execution(
        self,
        code: str,
        language: str,
        trace_data: List[Dict[str, Any]],
        output: str
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze code execution and return structured insights about data structures and operations.
        
        Returns None if Gemini is not configured or if analysis fails.
        """
        if not self.client:
            logger.info("Gemini not configured, skipping AI analysis")
            return None
        
        try:
            # Limit trace to first 50 and last 5 steps to avoid token limits
            trace_sample = trace_data[:50] if len(trace_data) > 50 else trace_data
            if len(trace_data) > 55:
                trace_sample.extend(trace_data[-5:])
            
            prompt = f"""
SYSTEM INSTRUCTION:
You are an expert code analysis engine for a CS education tool.
Your job is to analyze code execution traces and extract logical data structure operations.
You must output ONLY valid JSON. No markdown formatting. No intro text.

INPUT DATA:
1. Code: The source code provided by the user.
2. Language: {language}
3. Trace: A step-by-step JSON execution log (showing {len(trace_sample)} of {len(trace_data)} steps).
4. Output: {output}

YOUR TASK:
Analyze the provided code and trace to identify:
1. "Logical Structures": Group variables into logical units (e.g., "Recursion Stack", "Accumulator", "Loop Iterator").
2. "Operations": For each significant step in the trace, describe what happened conceptually (e.g., "pushed to stack", "incremented counter", "swapped values").

CODE:
```{language}
{code}
```

TRACE DATA:
{json.dumps(trace_sample, indent=2)}

OUTPUT SCHEMA (Strict JSON):
{{
  "structures": [
    {{
      "name": "Name of structure (e.g., Factorial Stack, Counter)",
      "type": "Type (e.g., Stack, Queue, Variable, Array, Class)",
      "variables": ["list", "of", "variable_names_involved"],
      "description": "Brief explanation of what this structure manages."
    }}
  ],
  "trace_enrichment": {{
    "step_index_mapping": {{
       "1": "Human readable explanation of what happened at this step",
       "10": "Recursively called factorial(3), pushing a new frame to stack."
    }}
  }},
  "summary": "A brief 2-3 sentence summary of what this code does and its key algorithmic approach."
}}
"""
            
            # Call Gemini
            response = self.client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    response_mime_type='application/json'
                )
            )
            
            # Parse and return JSON
            result = json.loads(response.text)
            logger.info("Successfully analyzed execution with Gemini")
            return result
            
        except Exception as e:
            logger.error(f"Gemini analysis failed: {e}")
            # Return None on failure - don't break the main API
            return None


# Singleton instance
_gemini_service = None

def get_gemini_service() -> GeminiService:
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
