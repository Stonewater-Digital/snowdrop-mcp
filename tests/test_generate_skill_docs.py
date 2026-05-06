"""Tests for scripts/generate_skill_docs.py.

Uses real skill files from the snowdrop-mcp repository (read-only access)
as test inputs to exercise the TOOL_META extractor and SKILL.md generator.

All writes are scoped to tmp_path fixtures — the source skills/ directory is
never modified.
"""
from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Ensure the scripts/ directory is importable so we can import the module
# under test without installing it as a package.
# ---------------------------------------------------------------------------

_WORKTREE = Path(__file__).parent.parent  # .../snowdrop-mcp-skills-refactor-20260506/
_SCRIPTS_DIR = _WORKTREE / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import generate_skill_docs as gsd  # noqa: E402

# ---------------------------------------------------------------------------
# Fixtures — paths to real skill files (read-only)
# ---------------------------------------------------------------------------

_SKILLS_DIR = Path(
    "/home/snowdrop/snowdrop-core/repos/snowdrop-mcp/skills"
)

# A free skill that uses the "inputSchema" key
_INPUTSCHEMA_SKILL = _SKILLS_DIR / "accounting" / "ebitda_calculator.py"

# A premium skill that has no inputSchema/parameters (stub only)
_PREMIUM_STUB_SKILL = _SKILLS_DIR / "fund_accounting" / "allocation_enforcer_80_20.py"

# A skill that uses the "inputSchema" key in the technical/ subdir
_TECHNICAL_SKILL = _SKILLS_DIR / "technical" / "fastapi_to_mcp_wrapper.py"

# Repo root (parent of skills/)
_REPO_ROOT = _SKILLS_DIR.parent


# ---------------------------------------------------------------------------
# 1. test_extract_tool_meta_inputSchema
# ---------------------------------------------------------------------------

class TestExtractToolMetaInputSchema:
    """TOOL_META extraction for skills using the 'inputSchema' key."""

    def test_returns_dict(self):
        meta = gsd.extract_tool_meta(_INPUTSCHEMA_SKILL, _REPO_ROOT)
        assert isinstance(meta, dict), "Expected a dict from extract_tool_meta"

    def test_name_field(self):
        meta = gsd.extract_tool_meta(_INPUTSCHEMA_SKILL, _REPO_ROOT)
        assert meta["name"] == "ebitda_calculator"

    def test_description_present(self):
        meta = gsd.extract_tool_meta(_INPUTSCHEMA_SKILL, _REPO_ROOT)
        assert "description" in meta
        assert len(meta["description"]) > 0

    def test_inputSchema_key_present(self):
        meta = gsd.extract_tool_meta(_INPUTSCHEMA_SKILL, _REPO_ROOT)
        assert "inputSchema" in meta, "Expected 'inputSchema' key in TOOL_META"

    def test_required_params_extracted(self):
        meta = gsd.extract_tool_meta(_INPUTSCHEMA_SKILL, _REPO_ROOT)
        schema = meta.get("inputSchema", {})
        params = gsd._extract_params_from_schema(schema)
        required_names = {p["name"] for p in params if p["required"]}
        assert "net_income" in required_names
        assert "interest" in required_names
        assert "taxes" in required_names

    def test_no_parameters_key(self):
        """ebitda_calculator should use inputSchema, not the legacy 'parameters' key."""
        meta = gsd.extract_tool_meta(_INPUTSCHEMA_SKILL, _REPO_ROOT)
        assert "parameters" not in meta or "inputSchema" in meta


# ---------------------------------------------------------------------------
# 2. test_extract_tool_meta_parameters
# ---------------------------------------------------------------------------

class TestExtractToolMetaParameters:
    """TOOL_META extraction for skills using the old 'parameters' key (or minimal stubs)."""

    def test_premium_stub_returns_dict(self):
        meta = gsd.extract_tool_meta(_PREMIUM_STUB_SKILL, _REPO_ROOT)
        assert isinstance(meta, dict)

    def test_premium_stub_has_name(self):
        meta = gsd.extract_tool_meta(_PREMIUM_STUB_SKILL, _REPO_ROOT)
        assert meta.get("name") == "allocation_enforcer_80_20"

    def test_premium_tier_detected(self):
        meta = gsd.extract_tool_meta(_PREMIUM_STUB_SKILL, _REPO_ROOT)
        tier = gsd._detect_tier(meta, _PREMIUM_STUB_SKILL)
        assert tier == "premium"

    def test_parameters_variant_extraction(self, tmp_path: Path):
        """Synthetic skill using old 'parameters' key."""
        skill_content = textwrap.dedent("""\
            TOOL_META = {
                "name": "legacy_skill",
                "description": "A legacy skill using the parameters key.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "amount": {
                            "type": "number",
                            "description": "Amount in USD."
                        }
                    },
                    "required": ["amount"]
                }
            }

            def legacy_skill(amount: float) -> dict:
                return {"status": "ok", "data": {"amount": amount}, "timestamp": ""}
        """)
        skill_file = tmp_path / "legacy_skill.py"
        skill_file.write_text(skill_content)

        meta = gsd.extract_tool_meta(skill_file, tmp_path)
        assert meta is not None
        assert meta["name"] == "legacy_skill"
        assert "parameters" in meta

        params = gsd._extract_params_from_schema(meta["parameters"])
        assert len(params) == 1
        assert params[0]["name"] == "amount"
        assert params[0]["required"] is True

    def test_extract_params_from_list_style(self):
        """Some legacy skills stored parameters as a list of dicts."""
        schema = [
            {"name": "start_date", "type": "string", "required": True, "description": "Start date."},
            {"name": "end_date", "type": "string", "required": False, "description": "End date."},
        ]
        params = gsd._extract_params_from_schema(schema)
        assert len(params) == 2
        names = [p["name"] for p in params]
        assert "start_date" in names
        assert "end_date" in names
        start = next(p for p in params if p["name"] == "start_date")
        assert start["required"] is True


# ---------------------------------------------------------------------------
# 3. test_generate_skill_md_content
# ---------------------------------------------------------------------------

class TestGenerateSkillMdContent:
    """Generated SKILL.md must contain all required sections."""

    @pytest.fixture
    def ebitda_md(self) -> str:
        meta = gsd.extract_tool_meta(_INPUTSCHEMA_SKILL, _REPO_ROOT)
        return gsd.generate_skill_md(meta, category="accounting", py_file=_INPUTSCHEMA_SKILL)

    def test_has_description_section(self, ebitda_md: str):
        assert "## Description" in ebitda_md

    def test_has_parameters_section(self, ebitda_md: str):
        assert "## Parameters" in ebitda_md

    def test_has_returns_section(self, ebitda_md: str):
        assert "## Returns" in ebitda_md

    def test_has_example_section(self, ebitda_md: str):
        assert "## Example" in ebitda_md

    def test_has_usage_section(self, ebitda_md: str):
        assert "## Usage" in ebitda_md

    def test_frontmatter_skill_name(self, ebitda_md: str):
        assert "skill: ebitda_calculator" in ebitda_md

    def test_frontmatter_category(self, ebitda_md: str):
        assert "category: accounting" in ebitda_md

    def test_frontmatter_tier_free(self, ebitda_md: str):
        assert "tier: free" in ebitda_md

    def test_example_is_valid_json(self, ebitda_md: str):
        # Extract the JSON block that appears specifically under ## Example
        # Walk lines, enter ## Example section, then grab the first ```json ... ``` block.
        lines = ebitda_md.splitlines()
        in_example_section = False
        in_json_block = False
        json_lines: list[str] = []
        for line in lines:
            if line.strip() == "## Example":
                in_example_section = True
                continue
            if in_example_section and line.startswith("## "):
                # Left the Example section without finding a block — give up
                break
            if in_example_section and line.strip() == "```json":
                in_json_block = True
                continue
            if in_json_block and line.strip() == "```":
                break
            if in_json_block:
                json_lines.append(line)

        assert json_lines, "No JSON block found under ## Example section"
        json_str = "\n".join(json_lines)
        parsed = json.loads(json_str)
        assert parsed["tool"] == "ebitda_calculator"

    def test_params_table_has_net_income(self, ebitda_md: str):
        assert "net_income" in ebitda_md

    def test_usage_mentions_snowdrop_execute(self, ebitda_md: str):
        assert "snowdrop_execute" in ebitda_md

    def test_premium_stub_md_has_premium_tier(self):
        meta = gsd.extract_tool_meta(_PREMIUM_STUB_SKILL, _REPO_ROOT)
        md = gsd.generate_skill_md(meta, category="fund_accounting", py_file=_PREMIUM_STUB_SKILL)
        assert "tier: premium" in md


# ---------------------------------------------------------------------------
# 4. test_dry_run_no_files_written
# ---------------------------------------------------------------------------

class TestDryRunNoFilesWritten:
    """--dry-run mode must not create any files."""

    def test_no_files_written_in_dry_run(self, tmp_path: Path, capsys):
        """Dry-run over a small synthetic skills directory writes nothing."""
        # Build a minimal skills/ layout
        skills_dir = tmp_path / "skills"
        acct_dir = skills_dir / "accounting"
        acct_dir.mkdir(parents=True)

        skill_content = textwrap.dedent("""\
            TOOL_META = {
                "name": "dry_run_skill",
                "description": "A skill for dry-run testing.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "value": {"type": "number", "description": "A number."}
                    },
                    "required": ["value"]
                }
            }

            def dry_run_skill(value: float) -> dict:
                return {"status": "ok", "data": {}, "timestamp": ""}
        """)
        (acct_dir / "dry_run_skill.py").write_text(skill_content)

        # Run in dry-run mode
        count = gsd.walk_and_generate(skills_dir=skills_dir, dry_run=True)

        # No .SKILL.md files should exist anywhere under tmp_path
        skill_md_files = list(tmp_path.rglob("*.SKILL.md"))
        assert skill_md_files == [], f"Unexpected files written: {skill_md_files}"

        # But it should report it would generate 1 file
        assert count == 1

    def test_dry_run_prints_would_generate(self, tmp_path: Path, capsys):
        """Dry-run prints [dry-run] prefix lines."""
        skills_dir = tmp_path / "skills"
        acct_dir = skills_dir / "accounting"
        acct_dir.mkdir(parents=True)

        skill_content = textwrap.dedent("""\
            TOOL_META = {
                "name": "preview_skill",
                "description": "Preview skill for dry-run.",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            }

            def preview_skill() -> dict:
                return {"status": "ok", "data": {}, "timestamp": ""}
        """)
        (acct_dir / "preview_skill.py").write_text(skill_content)

        gsd.walk_and_generate(skills_dir=skills_dir, dry_run=True)
        captured = capsys.readouterr()
        assert "[dry-run]" in captured.out


# ---------------------------------------------------------------------------
# 5. test_generates_correct_filename
# ---------------------------------------------------------------------------

class TestGeneratesCorrectFilename:
    """Output filename must be <skill_name>.SKILL.md, not just SKILL.md."""

    def test_filename_uses_skill_name(self, tmp_path: Path):
        skills_dir = tmp_path / "skills"
        acct_dir = skills_dir / "accounting"
        acct_dir.mkdir(parents=True)

        skill_content = textwrap.dedent("""\
            TOOL_META = {
                "name": "my_unique_skill",
                "description": "Skill with a specific name for filename test.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "x": {"type": "number", "description": "Input x."}
                    },
                    "required": ["x"]
                }
            }

            def my_unique_skill(x: float) -> dict:
                return {"status": "ok", "data": {}, "timestamp": ""}
        """)
        (acct_dir / "my_unique_skill.py").write_text(skill_content)

        gsd.walk_and_generate(skills_dir=skills_dir, dry_run=False)

        expected = acct_dir / "my_unique_skill.SKILL.md"
        assert expected.exists(), f"Expected {expected} to be created"

    def test_filename_not_plain_skill_md(self, tmp_path: Path):
        """The output file must NOT be named just 'SKILL.md'."""
        skills_dir = tmp_path / "skills"
        cat_dir = skills_dir / "cat"
        cat_dir.mkdir(parents=True)

        skill_content = textwrap.dedent("""\
            TOOL_META = {
                "name": "named_skill",
                "description": "Named skill to check filename.",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            }

            def named_skill() -> dict:
                return {"status": "ok", "data": {}, "timestamp": ""}
        """)
        (cat_dir / "named_skill.py").write_text(skill_content)

        gsd.walk_and_generate(skills_dir=skills_dir, dry_run=False)

        plain_skill_md = cat_dir / "SKILL.md"
        assert not plain_skill_md.exists(), "'SKILL.md' must not be written; use '<name>.SKILL.md'"

    def test_two_skills_same_directory_both_get_distinct_files(self, tmp_path: Path):
        """Two skills in the same directory each get their own .SKILL.md."""
        skills_dir = tmp_path / "skills"
        cat_dir = skills_dir / "cat"
        cat_dir.mkdir(parents=True)

        for skill_name in ("skill_alpha", "skill_beta"):
            content = textwrap.dedent(f"""\
                TOOL_META = {{
                    "name": "{skill_name}",
                    "description": "Test skill {skill_name}.",
                    "inputSchema": {{"type": "object", "properties": {{}}, "required": []}}
                }}

                def {skill_name}() -> dict:
                    return {{"status": "ok", "data": {{}}, "timestamp": ""}}
            """)
            (cat_dir / f"{skill_name}.py").write_text(content)

        gsd.walk_and_generate(skills_dir=skills_dir, dry_run=False)

        assert (cat_dir / "skill_alpha.SKILL.md").exists()
        assert (cat_dir / "skill_beta.SKILL.md").exists()
