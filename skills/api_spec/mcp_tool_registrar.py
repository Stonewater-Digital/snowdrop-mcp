"""Format skills as MCP tool registration payload."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "mcp_tool_registrar",
    "description": "Produces a JSON-RPC compliant MCP tools/list response for Snowdrop skills.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skills": {"type": "array", "items": {"type": "object"}},
            "server_name": {"type": "string", "default": "snowdrop-mcp"},
        },
        "required": ["skills"],
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


def mcp_tool_registrar(
    skills: list[dict[str, Any]],
    server_name: str = "snowdrop-mcp",
    **_: Any,
) -> dict[str, Any]:
    """Return MCP tooling response for provided skills."""
    try:
        tools_payload = []
        categories: set[str] = set()
        for meta in skills:
            name = meta.get("name")
            description = meta.get("description", "")
            if not name:
                raise ValueError("Each skill must include a name")
            input_schema = meta.get("inputSchema", {})
            output_schema = meta.get("outputSchema", {})
            category = meta.get("category", "general")
            categories.add(str(category))
            tools_payload.append(
                {
                    "name": name,
                    "description": description,
                    "input_schema": input_schema,
                    "output_schema": output_schema,
                    "category": category,
                }
            )

        rpc_response = {
            "jsonrpc": "2.0",
            "id": server_name,
            "result": {
                "tools": tools_payload,
            },
        }
        data = {
            "rpc_response": rpc_response,
            "tool_count": len(tools_payload),
            "categories": sorted(categories),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("mcp_tool_registrar", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
