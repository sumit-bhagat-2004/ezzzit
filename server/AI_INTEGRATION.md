# AI Integration Guide

## Overview
The execute API now includes AI-powered code analysis using Google Gemini 1.5 Flash. When code is executed, Gemini analyzes the trace and provides:

1. **Data Structures**: Logical groupings of variables (e.g., "Recursion Stack", "Counter")
2. **Step Explanations**: Human-readable descriptions for each trace step
3. **Summary**: Overall explanation of the algorithm

## Setup

### 1. Get Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Click "Get API Key"
3. Copy the key

### 2. Configure Environment
Create a `.env` file in the `server` directory:

```bash
JUDGE0_URL=http://localhost:2358
GEMINI_API_KEY=your_api_key_here
```

### 3. Install Dependencies
```bash
cd server
pip install -r requirements.txt
```

## Response Structure

The `/execute` endpoint now returns:

```json
{
  "output": "6\n24",
  "trace": [...],
  "steps": 35,
  "exception": null,
  "error": null,
  "ai_analysis": {
    "structures": [
      {
        "name": "Counter Instance",
        "type": "Class",
        "variables": ["counter"],
        "description": "Accumulates values in a loop"
      }
    ],
    "trace_enrichment": {
      "step_index_mapping": {
        "1": "Program initialization begins",
        "10": "Method add() called with value 1"
      }
    },
    "summary": "This code demonstrates a Counter class and recursive factorial calculation..."
  }
}
```

## How It Works

1. **Execute**: Code runs through Judge0 with trace injection
2. **Analyze**: Trace + code sent to Gemini 1.5 Flash
3. **Enrich**: AI analysis added to response
4. **Graceful Fallback**: If Gemini fails, `ai_analysis` is `null` (doesn't break the app)

## Performance

- **Speed**: Gemini 1.5 Flash returns analysis in ~2-3 seconds
- **Cost**: Free tier = 15 requests/minute, 1,500/day
- **Optimization**: Only first 50 and last 5 trace steps sent to reduce tokens

## Frontend Integration

Check `execution.ai_analysis` to display:
- Data structures in Panel 4
- Step explanations when user hovers/clicks steps
- Overall algorithm summary

Example:
```typescript
if (execution.ai_analysis) {
  console.log(execution.ai_analysis.summary);
  console.log(execution.ai_analysis.structures);
}
```

## Troubleshooting

**No AI analysis returned?**
- Check if `GEMINI_API_KEY` is set
- Check server logs for errors
- Verify API key is valid at [Google AI Studio](https://aistudio.google.com/)

**Slow responses?**
- Normal - Gemini takes 2-3 seconds
- Consider showing loading spinner on frontend
- AI runs in parallel with trace execution

## Notes

- AI analysis is **optional** - execution works without it
- If Gemini fails, the error is logged but doesn't break the API
- Perfect for hackathons with the free tier limits
