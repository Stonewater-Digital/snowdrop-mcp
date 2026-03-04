"""Generate markdown documentation from TOOL_META definitions."""
from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "skill_doc_generator",
    "description": "Renders markdown docs for a skill module's TOOL_META.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skill_module_path": {
                "type": "string",
                "description": "Path to the Python module containing TOOL_META.",
            },
            "tool_meta": {
                "type": "object",
                "description": "Optional TOOL_META dict provided directly.",
            },
        },
        "required": [],
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


def skill_doc_generator(
    skill_module_path: str | None = None,
    tool_meta: dict[str, Any] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Produce markdown docs summarizing TOOL_META."""
    try:
        if tool_meta is None:
            if not skill_module_path:
                raise ValueError("Provide either tool_meta or skill_module_path")
            tool_meta = _load_tool_meta(skill_module_path)

        markdown = _render_markdown(tool_meta)
        result = {
            "markdown": markdown,
            "skill_name": tool_meta.get("name"),
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("skill_doc_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _load_tool_meta(module_path: str) -> dict[str, Any]:
    path = Path(module_path)
    if not path.exists():
        raise ValueError(f"Module path not found: {module_path}")
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ValueError("Unable to load module for documentation")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[arg-type]
    tool_meta = getattr(module, "TOOL_META", None)
    if not isinstance(tool_meta, dict):
        raise ValueError("Module missing TOOL_META definition")
    return tool_meta


def _render_markdown(meta: dict[str, Any]) -> str:
    name = meta.get("name", "unknown_tool")
    description = meta.get("description", "")
    input_schema = meta.get("inputSchema", {}) or {}
    properties = input_schema.get("properties", {}) or {}
    required = set(input_schema.get("required", []))

    md_lines = [f"# {name}", "", description, ""]
    if properties:
        md_lines.append("## Parameters")
        md_lines.append("| Name | Type | Required | Description |")
        md_lines.append("| --- | --- | --- | --- |")
        for param, schema in properties.items():
            dtype = schema.get("type", "any")
            desc = schema.get("description", "")
            default = schema.get("default")
            if default is not None:
                desc = f"{desc} (default: {default})".strip()
            md_lines.append(
                f"| {param} | {dtype} | {'yes' if param in required else 'no'} | {desc or '-'} |"
            )
        md_lines.append("")

    output_schema = meta.get("outputSchema", {}) or {}
    if output_schema:
        md_lines.append("## Returns")
        md_lines.append("```json")
        md_lines.append(json.dumps(output_schema, indent=2))
        md_lines.append("```")
        md_lines.append("")

    md_lines.append("## Example")
    md_lines.append("```json")
    md_lines.append(
        '{"tool": "' + name + '", "input": {"param_name": "value"}}'
    )
    md_lines.append("```")
    return "\n".join(md_lines)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
