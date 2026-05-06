#!/usr/bin/env python3
"""
Executive Summary: Validate that every skill .py file with TOOL_META has a corresponding
.SKILL.md documentation file. Exits with code 1 if any SKILL.md files are missing.

Table of Contents:
    1. Imports and Setup
    2. TOOL_META Detection
    3. Validation Logic
    4. CLI Entry Point
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. Imports and Setup
# ---------------------------------------------------------------------------

_EXCLUDED_FILES: frozenset[str] = frozenset({"__init__.py", "mcp_server.py"})


# ---------------------------------------------------------------------------
# 2. TOOL_META Detection
# ---------------------------------------------------------------------------

def _extract_tool_meta_name(py_file: Path) -> str | None:
    """Extract the skill name from TOOL_META["name"] via AST parsing.

    Uses AST parsing to avoid import side-effects. Handles simple dict
    literals and type-annotated assignments (e.g. TOOL_META: dict = {...}).

    Returns the skill name string, or None if not found.
    """
    try:
        source = py_file.read_text(encoding="utf-8")
    except OSError:
        return None

    # Fast path: string check before AST parse
    if "TOOL_META" not in source:
        return None

    try:
        tree = ast.parse(source, filename=str(py_file))
    except SyntaxError:
        return None

    # Find TOOL_META assignment value
    meta_value: ast.expr | None = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "TOOL_META":
                    meta_value = node.value
                    break
        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == "TOOL_META":
                meta_value = node.value
                break
        if meta_value is not None:
            break

    if meta_value is None:
        return None

    # Try to extract the "name" key from the dict literal
    try:
        meta_dict = ast.literal_eval(meta_value)
        if isinstance(meta_dict, dict) and meta_dict.get("name"):
            return str(meta_dict["name"])
    except (ValueError, TypeError):
        pass

    # Regex fallback for computed/multiline dicts
    import re
    name_match = re.search(r'"name"\s*:\s*"([^"]+)"', source)
    if name_match:
        return name_match.group(1)

    return None


# ---------------------------------------------------------------------------
# 3. Validation Logic
# ---------------------------------------------------------------------------

def validate_skill_docs(
    skills_dir: Path,
    *,
    quiet: bool = False,
) -> list[Path]:
    """Scan skills_dir for .py files with TOOL_META that are missing .SKILL.md.

    The generator names SKILL.md files using TOOL_META["name"], which may differ
    from the Python file's stem. This validator extracts the name from TOOL_META
    to find the expected SKILL.md path.

    Args:
        skills_dir: Path to the skills/ directory.
        quiet: If True, suppress per-file output.

    Returns:
        List of .py file paths that are missing their .SKILL.md counterpart.
    """
    missing: list[Path] = []

    for py_file in sorted(skills_dir.rglob("*.py")):
        # Skip excluded files and __pycache__
        if py_file.name in _EXCLUDED_FILES:
            continue
        if "__pycache__" in py_file.parts:
            continue

        skill_name = _extract_tool_meta_name(py_file)
        if not skill_name:
            continue

        # Generator places SKILL.md next to the .py, named after TOOL_META["name"]
        expected_md = py_file.parent / f"{skill_name}.SKILL.md"
        if not expected_md.exists():
            missing.append(py_file)
            if not quiet:
                rel = py_file.relative_to(skills_dir.parent)
                print(f"MISSING SKILL.md: {rel} (expected: {skill_name}.SKILL.md)", file=sys.stderr)

    return missing


# ---------------------------------------------------------------------------
# 4. CLI Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Validate that every skill .py file with TOOL_META has a "
            "corresponding .SKILL.md documentation file."
        ),
    )
    parser.add_argument(
        "--skills-dir",
        default="skills/",
        help="Path to the skills/ directory (default: skills/)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-file output; only show summary.",
    )
    args = parser.parse_args()

    skills_dir = Path(args.skills_dir).resolve()
    if not skills_dir.exists():
        print(f"ERROR: skills directory not found: {skills_dir}", file=sys.stderr)
        sys.exit(1)

    if not args.quiet:
        print(f"Scanning for missing SKILL.md files in: {skills_dir}")

    missing = validate_skill_docs(skills_dir, quiet=args.quiet)

    total_skills = sum(
        1
        for py in skills_dir.rglob("*.py")
        if py.name not in _EXCLUDED_FILES
        and "__pycache__" not in py.parts
        and _extract_tool_meta_name(py) is not None
    )

    print(f"\nSkills with TOOL_META: {total_skills}")
    print(f"Missing SKILL.md:       {len(missing)}")

    if missing:
        print(
            f"\nERROR: {len(missing)} skill(s) are missing their .SKILL.md file.",
            file=sys.stderr,
        )
        print(
            "Run: python3 scripts/generate_skill_docs.py  to generate missing docs.",
            file=sys.stderr,
        )
        sys.exit(1)
    else:
        print("\nAll skills have SKILL.md documentation.")
        sys.exit(0)


if __name__ == "__main__":
    main()
