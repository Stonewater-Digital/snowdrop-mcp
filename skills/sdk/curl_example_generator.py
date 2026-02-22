"""Generate curl examples for Snowdrop skills."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "curl_example_generator",
    "description": "Builds ready-to-run curl commands for each skill's input schema.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skills": {"type": "array", "items": {"type": "object"}},
            "server_url": {"type": "string"},
            "sample_api_key": {"type": "string", "default": "sk-your-api-key-here"},
        },
        "required": ["skills", "server_url"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def curl_example_generator(
    skills: list[dict[str, Any]],
    server_url: str,
    sample_api_key: str = "sk-your-api-key-here",
    **_: Any,
) -> dict[str, Any]:
    """Return a dict of skill name to curl example along with markdown."""
    try:
        examples: dict[str, str] = {}
        markdown_lines = ["# Snowdrop Curl Examples"]
        for meta in skills:
            name = meta.get("name")
            if not name:
                continue
            payload = _sample_payload(meta.get("inputSchema", {}))
            body = json.dumps(payload, indent=2)
            cmd = (
                "curl -X POST "
                f"{server_url}/tools/{name} "
                "-H 'Authorization: Bearer {api}' "
                "-H 'Content-Type: application/json' "
                f"-d '{body}'"
            ).format(api=sample_api_key)
            examples[name] = cmd
            markdown_lines.append(f"\n## {name}\n\n```bash\n{cmd}\n```\n")
        data = {
            "examples": examples,
            "total_skills": len(examples),
            "markdown_doc": "\n".join(markdown_lines),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("curl_example_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _sample_payload(schema: dict[str, Any]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for prop, definition in (schema.get("properties") or {}).items():
        dtype = definition.get("type")
        if dtype == "number":
            payload[prop] = 1.0
        elif dtype == "integer":
            payload[prop] = 1
        elif dtype == "array":
            payload[prop] = []
        elif dtype == "object":
            payload[prop] = {}
        else:
            payload[prop] = f"{prop}_value"
    return payload


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
