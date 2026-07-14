# Text Summarizer Agent with FastAPI

Small single-agent project built to learn FastAPI on top of the OpenAI Agents SDK. Takes a piece of text and returns a short summary, with response time and token usage included.

## Architecture

```
User text
    ↓
Summarizer Agent (single agent, no orchestration, no MCP)
    ↓
Structured output: { summary, tokens, time }
```

Deliberately flat — no multi-agent pipeline, no tools, no RAG — so the focus stays on the FastAPI layer rather than agent complexity.

## Files

| File | Purpose |
|---|---|
| `agent.py` | Agent definition and `aicall()` — the core logic, reused by both entry points |
| `main.py` | Terminal entry point for quick manual testing |
| `api.py` | FastAPI app exposing the agent as an HTTP endpoint |
| `httptest.py` | Sends a test request to the running API |
| `config.yaml` | Model, instructions, temperature, and max tokens for the agent |

## Setup

```bash
pip install -r requirements.txt
```

Copy `example.env` to `.env` and fill in your own values:
```
baseurl=your_openai_compatible_endpoint_here
api=your_api_key_here
```

## Running

Terminal version:
```bash
python main.py
```

API version:
```bash
uvicorn api:app --reload
```
Test it at `localhost:8000/docs`, or run:
```bash
python httptest.py
```

## Example request

```bash
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"text": "your text here"}'
```

Response:
```json
{
  "summary": "...",
  "Tokens": 187,
  "Time": 1.34
}
```

## Why no MCP/tools here

Summarization only needs the text already given in the request — there's no external data to fetch, so adding a tool-use MCP server here would be unnecessary complexity for this task (and in early testing, made the model call tools it didn't need instead of just summarizing). Later projects (e.g. a web research agent) use MCP servers where the task genuinely requires external lookups.
