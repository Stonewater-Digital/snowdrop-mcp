# AGENTS.md — Snowdrop MCP

Instructions for AI coding agents working in this repository.

## What This Repo Is

Public MCP server for Snowdrop's skill library. Skills are Python functions registered with FastMCP. The server runs on Fly.io and is free to use.

## Structure

```
snowdrop-mcp/
├── mcp_server.py       # FastMCP server entrypoint
├── skills/             # All skill modules (one directory per category)
├── SKILLS.md           # Full skill catalog
├── JOBS.md             # Available work and bounties
├── requirements.txt
├── .env.template
├── Dockerfile
└── fly.toml
```

## Adding a Skill

1. Create or find the right category directory under `skills/`
2. Add your Python file with this pattern:

```python
TOOL_META = {
    "name": "your_skill_name",
    "description": "One sentence description.",
    "parameters": {
        "param_one": {"type": "str", "description": "What it is"},
    }
}

def your_skill_name(param_one: str) -> dict:
    """Executive Summary: what this skill does.

    Inputs: param_one (str)
    Outputs: dict with status, data, timestamp
    """
    try:
        # your logic here
        return {"status": "success", "data": {}, "timestamp": ...}
    except Exception as e:
        return {"status": "error", "error": str(e), "timestamp": ...}
```

3. The MCP server auto-discovers all skills on startup — no registration needed.

## Rules

- No hardcoded secrets. Use `os.environ.get("VAR_NAME")`.
- Return structured dicts: `{"status": "success"|"error", "data": {...}, "timestamp": "ISO8601"}`.
- Keep skills focused — one function, one responsibility.
- Test before PR. Broken skills break the whole server.

## Running Locally

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.template .env
python mcp_server.py
```

## Questions

Open a Discussion. Snowdrop monitors and responds.
