#!/usr/bin/env python3
"""
Executive Summary: Generate SKILL.md documentation files from TOOL_META definitions
in snowdrop-mcp skill files. Supports both "inputSchema" and "parameters" TOOL_META
variants. Writes <skill_name>.SKILL.md alongside each skill's .py file.

Table of Contents:
    1. Imports and Setup
    2. TOOL_META Extraction (importlib + AST fallback)
    3. SKILL.md Content Generation
    4. Directory Walker
    5. CLI Entry Point
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import re
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

# ---------------------------------------------------------------------------
# 1. Imports and Setup
# ---------------------------------------------------------------------------

_EXCLUDED_FILES: frozenset[str] = frozenset({"__init__.py", "mcp_server.py"})


# ---------------------------------------------------------------------------
# 2. TOOL_META Extraction
# ---------------------------------------------------------------------------

def _load_tool_meta_via_importlib(py_file: Path, repo_root: Path) -> dict[str, Any] | None:
    """Load TOOL_META by importing the module dynamically.

    Uses the same technique as mcp_server._discover_skills(). Adds repo_root
    to sys.path so cross-skill imports (e.g. skills._paywall) don't fail.

    Returns the TOOL_META dict on success, or None on any failure.
    """
    # Ensure repo root is on sys.path for cross-module imports
    repo_root_str = str(repo_root)
    inserted = False
    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)
        inserted = True

    # Build a unique module name from the relative path
    try:
        rel = py_file.relative_to(repo_root)
        module_name = ".".join(rel.with_suffix("").parts)
    except ValueError:
        module_name = f"skill_{py_file.stem}"

    try:
        spec = importlib.util.spec_from_file_location(module_name, py_file)
        if spec is None or spec.loader is None:
            return None
        module: ModuleType = importlib.util.module_from_spec(spec)
        # Register in sys.modules so relative imports within skills work
        sys.modules[module_name] = module
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        tool_meta = getattr(module, "TOOL_META", None)
        if isinstance(tool_meta, dict):
            return tool_meta
        return None
    except Exception:  # noqa: BLE001
        return None
    finally:
        if inserted and repo_root_str in sys.path:
            sys.path.remove(repo_root_str)
        # Clean up sys.modules to avoid stale state across runs
        sys.modules.pop(module_name, None)


def _load_tool_meta_via_ast(py_file: Path) -> dict[str, Any] | None:
    """Fallback: extract TOOL_META via AST parsing (no import side-effects).

    Handles simple dict literals only — not computed values. Returns None if
    the TOOL_META assignment cannot be safely parsed.
    """
    try:
        source = py_file.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(py_file))
    except SyntaxError:
        return None

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "TOOL_META":
                try:
                    value = ast.literal_eval(node.value)
                    if isinstance(value, dict):
                        return value
                except (ValueError, TypeError):
                    pass
    return None


def _load_tool_meta_via_regex(py_file: Path) -> dict[str, Any] | None:
    """Last-resort fallback: extract key fields from TOOL_META via regex.

    Only captures name, description, and tier — not the full schema.
    Returns a minimal dict or None.
    """
    try:
        source = py_file.read_text(encoding="utf-8")
    except OSError:
        return None

    result: dict[str, Any] = {}

    # Extract name
    name_match = re.search(r'"name"\s*:\s*"([^"]+)"', source)
    if name_match:
        result["name"] = name_match.group(1)

    # Extract description
    desc_match = re.search(r'"description"\s*:\s*"([^"]+)"', source)
    if desc_match:
        result["description"] = desc_match.group(1)

    # Extract tier
    tier_match = re.search(r'"tier"\s*:\s*"([^"]+)"', source)
    if tier_match:
        result["tier"] = tier_match.group(1)

    return result if result.get("name") else None


def extract_tool_meta(py_file: Path, repo_root: Path) -> dict[str, Any] | None:
    """Extract TOOL_META from a skill file using importlib → AST → regex cascade.

    Args:
        py_file: Absolute path to the skill .py file.
        repo_root: Root of the snowdrop-mcp repository (for sys.path setup).

    Returns:
        The TOOL_META dict, or None if not found or extraction fails.
    """
    meta = _load_tool_meta_via_importlib(py_file, repo_root)
    if meta is not None:
        return meta

    meta = _load_tool_meta_via_ast(py_file)
    if meta is not None:
        return meta

    return _load_tool_meta_via_regex(py_file)


# ---------------------------------------------------------------------------
# 3. SKILL.md Content Generation
# ---------------------------------------------------------------------------

def _first_two_sentences(text: str) -> str:
    """Return the first two sentences from text (period-terminated)."""
    if not text:
        return ""
    # Split on sentence-ending punctuation followed by whitespace or end-of-string
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return " ".join(sentences[:2])


def _detect_tier(tool_meta: dict[str, Any], py_file: Path) -> str:
    """Determine skill tier from TOOL_META or file content.

    Checks:
      1. TOOL_META["tier"] key
      2. File content for PREMIUM markers
    """
    if tool_meta.get("tier"):
        return str(tool_meta["tier"]).lower()

    try:
        content = py_file.read_text(encoding="utf-8")
        if re.search(r"\bPREMIUM\b", content):
            return "premium"
    except OSError:
        pass

    return "free"


def _extract_params_from_schema(schema: Any) -> list[dict[str, Any]]:
    """Normalise inputSchema or parameters into a flat list of param dicts.

    Each item has: name, type, required (bool), description.

    Handles three schema shapes:
      1. JSON Schema object dict with "properties" key (most common / "inputSchema" variant).
      2. Legacy list of param dicts, each with "name", "type", "required", "description".
      3. Anything else — returns empty list.
    """
    params: list[dict[str, Any]] = []

    # Shape 2: legacy list of param dicts
    if isinstance(schema, list):
        for item in schema:
            if isinstance(item, dict) and item.get("name"):
                params.append({
                    "name": item["name"],
                    "type": item.get("type", "any"),
                    "required": bool(item.get("required", False)),
                    "description": item.get("description", ""),
                })
        return params

    if not isinstance(schema, dict):
        return params

    # Shape 1: Standard JSON Schema object with "properties"
    if "properties" in schema:
        required_fields: list[str] = schema.get("required", [])
        for param_name, param_def in schema.get("properties", {}).items():
            params.append({
                "name": param_name,
                "type": param_def.get("type", "any"),
                "required": param_name in required_fields,
                "description": param_def.get("description", ""),
            })
        return params

    return params


def _build_params_table(params: list[dict[str, Any]]) -> str:
    """Render a Markdown table for the given parameter list."""
    if not params:
        return "_No parameters defined._"

    lines = [
        "| Name | Type | Required | Description |",
        "|------|------|----------|-------------|",
    ]
    for p in params:
        req = "Yes" if p["required"] else "No"
        desc = p["description"].replace("|", "\\|")
        lines.append(f"| `{p['name']}` | `{p['type']}` | {req} | {desc} |")
    return "\n".join(lines)


def _build_example_args(params: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a minimal example arguments dict from required params."""
    example: dict[str, Any] = {}
    for p in params:
        if not p["required"]:
            continue
        ptype = p["type"]
        if ptype == "string":
            example[p["name"]] = f"<{p['name']}>"
        elif ptype in ("number", "integer"):
            example[p["name"]] = 0
        elif ptype == "boolean":
            example[p["name"]] = False
        elif ptype == "array":
            example[p["name"]] = []
        elif ptype == "object":
            example[p["name"]] = {}
        else:
            example[p["name"]] = f"<{p['name']}>"
    return example


def _title_case(snake: str) -> str:
    """Convert snake_case skill name to Title Case for headings."""
    return " ".join(word.capitalize() for word in snake.split("_"))


def generate_skill_md(
    tool_meta: dict[str, Any],
    category: str,
    py_file: Path,
) -> str:
    """Render the full SKILL.md content string for a given TOOL_META.

    Args:
        tool_meta: The TOOL_META dict extracted from the skill file.
        category: The subdirectory name (e.g. "accounting").
        py_file: Path to the source .py file (used for tier detection).

    Returns:
        A Markdown string suitable for writing to <skill_name>.SKILL.md.
    """
    name: str = tool_meta.get("name", py_file.stem)
    description: str = tool_meta.get("description", "")
    tier: str = _detect_tier(tool_meta, py_file)
    output_schema: dict = tool_meta.get("outputSchema", {})

    # Resolve parameter schema — support both key names
    raw_schema = tool_meta.get("inputSchema") or tool_meta.get("parameters") or {}
    params = _extract_params_from_schema(raw_schema)

    # Frontmatter
    required_inputs = [p["name"] for p in params if p["required"]]
    inputs_str = ", ".join(required_inputs) if required_inputs else "none"
    short_desc = _first_two_sentences(description)

    frontmatter = (
        "---\n"
        f"skill: {name}\n"
        f"category: {category}\n"
        f"description: {short_desc}\n"
        f"tier: {tier}\n"
        f"inputs: {inputs_str}\n"
        "---"
    )

    # Parameters table
    params_table = _build_params_table(params)

    # Returns section
    if output_schema and output_schema.get("description"):
        returns_text = output_schema["description"]
    else:
        returns_text = (
            "Standard Snowdrop envelope:\n"
            "```json\n"
            '{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}\n'
            "```"
        )

    # Example block
    example_args = _build_example_args(params)
    example_json = json.dumps(
        {"tool": name, "arguments": example_args},
        indent=2,
    )

    content = f"""{frontmatter}

# {_title_case(name)}

## Description
{description}

## Parameters
{params_table}

## Returns
{returns_text}

## Example
```json
{example_json}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "{name}"`.
"""
    return content


# ---------------------------------------------------------------------------
# 4. Directory Walker
# ---------------------------------------------------------------------------

def walk_and_generate(
    skills_dir: Path,
    dry_run: bool = False,
) -> int:
    """Walk skills_dir, find all TOOL_META skill files, generate SKILL.md docs.

    Args:
        skills_dir: Root of the skills/ directory to walk.
        dry_run: If True, print what would be written without creating files.

    Returns:
        Number of SKILL.md files generated (or would-be generated in dry-run).
    """
    repo_root = skills_dir.parent  # e.g. /path/to/snowdrop-mcp
    count = 0

    for py_file in sorted(skills_dir.rglob("*.py")):
        if py_file.name in _EXCLUDED_FILES:
            continue

        # Determine category from relative path
        rel_parts = py_file.relative_to(skills_dir).parts
        category = rel_parts[0] if len(rel_parts) > 1 else "root"

        tool_meta = extract_tool_meta(py_file, repo_root)
        if not tool_meta:
            continue

        skill_name = tool_meta.get("name", "")
        if not skill_name:
            continue

        # Output SKILL.md goes next to the .py file
        out_path = py_file.parent / f"{skill_name}.SKILL.md"

        if dry_run:
            rel_out = out_path.relative_to(skills_dir.parent) if out_path.is_relative_to(skills_dir.parent) else out_path
            print(f"[dry-run] Would generate: {rel_out}")
            count += 1
            continue

        content = generate_skill_md(tool_meta, category, py_file)
        out_path.write_text(content, encoding="utf-8")
        rel_out = out_path.relative_to(skills_dir.parent) if out_path.is_relative_to(skills_dir.parent) else out_path
        print(f"Generated: {rel_out}")
        count += 1

    return count


# ---------------------------------------------------------------------------
# 5. CLI Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate SKILL.md documentation from TOOL_META definitions.",
    )
    parser.add_argument(
        "--skills-dir",
        default="skills/",
        help="Path to the skills/ directory (default: skills/)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help=(
            "Output directory root (default: same directory as each skill .py file). "
            "Currently unused — SKILL.md files are always written next to their .py."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be generated without writing any files.",
    )
    args = parser.parse_args()

    skills_dir = Path(args.skills_dir).resolve()
    if not skills_dir.exists():
        print(f"ERROR: skills directory not found: {skills_dir}", file=sys.stderr)
        sys.exit(1)

    mode = "[dry-run] " if args.dry_run else ""
    print(f"{mode}Scanning skills in: {skills_dir}")

    total = walk_and_generate(skills_dir=skills_dir, dry_run=args.dry_run)

    verb = "Would generate" if args.dry_run else "Generated"
    print(f"\n{verb} {total} SKILL.md file(s).")


if __name__ == "__main__":
    main()
