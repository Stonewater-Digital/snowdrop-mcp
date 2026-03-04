"""
skill_catalog_sync.py — Live skill catalog status and sync trigger.

Executive Summary:
    MCP-callable skill that returns the current skill count breakdown (total,
    free, premium, failed imports) from the live server's discovery results.
    This is the canonical answer to "how many skills does Snowdrop have?" for
    any MCP consumer — no file system access needed. Pass regenerate=True to
    rebuild SNOWDROP_SKILLS.md and SKILLS.md from the current codebase.

Table of Contents:
    1. TOOL_META
    2. Constants
    3. skill_catalog_sync callable
"""
from __future__ import annotations

import logging
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger("snowdrop.skill_catalog_sync")

# ---------------------------------------------------------------------------
# 1. TOOL_META
# ---------------------------------------------------------------------------

TOOL_META: dict[str, Any] = {
    "name": "skill_catalog_sync",
    "description": (
        "Returns live skill count breakdown (total, free, premium, failed) from "
        "the running server. Pass regenerate=True to rebuild SNOWDROP_SKILLS.md "
        "and SKILLS.md from the current codebase (admin use only)."
    ),
    "tier": "free",
}

# ---------------------------------------------------------------------------
# 2. Constants
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).parent.parent.parent

# ---------------------------------------------------------------------------
# 3. skill_catalog_sync callable
# ---------------------------------------------------------------------------


def skill_catalog_sync(regenerate: bool = False) -> dict[str, Any]:
    """Return live skill counts and optionally trigger catalog regeneration.

    Args:
        regenerate: If True, runs generate_skill_directory.py and returns
                    updated counts. Requires write access to the repo root.
                    Defaults to False (read-only status report).

    Returns:
        Standard Snowdrop response envelope with:
            data.total       — skills currently registered on this instance
            data.premium     — premium skills (gated, real implementations)
            data.free        — free skills
            data.failed      — import failures at startup
            data.failed_list — list of failed module names (capped at 20)
            data.regenerated — True if catalog was refreshed this call
            data.catalog_path — path to SNOWDROP_SKILLS.md (if regenerated)
    """
    now = datetime.now(timezone.utc).isoformat()
    try:
        # Import the live server's discovery function — same logic as production.
        # sys.path insert ensures this works whether called locally or from Cloud Run.
        sys.path.insert(0, str(_REPO_ROOT))
        from skills.mcp_server import _discover_skills  # noqa: PLC0415

        discovered = _discover_skills()
        failed: list[str] = getattr(_discover_skills, "_failed_imports", [])

        # Classify premium vs free by module path (Bug 1 fix applied: replace \\ not "")
        premium = [
            name for name, rec in discovered.items()
            if "premium" in rec.get("module_path", "").replace("\\", "/")
        ]
        free_skills = [n for n in discovered if n not in premium]

        result: dict[str, Any] = {
            "total": len(discovered),
            "premium": len(premium),
            "free": len(free_skills),
            "failed": len(failed),
            "failed_list": failed[:20],  # cap to keep response size sane
            "regenerated": False,
        }

        if regenerate:
            gen_script = _REPO_ROOT / "scripts" / "generate_skill_directory.py"
            if gen_script.exists():
                proc = subprocess.run(
                    [sys.executable, str(gen_script)],
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                result["regenerated"] = proc.returncode == 0
                result["catalog_path"] = str(_REPO_ROOT / "SNOWDROP_SKILLS.md")
                # Return tail of output (stdout or stderr) for diagnostics
                output = proc.stdout or proc.stderr
                result["regen_output"] = output[-500:] if output else ""
            else:
                result["regenerated"] = False
                result["regen_error"] = "generate_skill_directory.py not found"

        logger.info(
            "skill_catalog_sync: total=%d premium=%d free=%d failed=%d regenerated=%s",
            result["total"],
            result["premium"],
            result["free"],
            result["failed"],
            result["regenerated"],
        )

        return {"status": "ok", "data": result, "timestamp": now}

    except Exception as exc:
        logger.error("skill_catalog_sync error: %s", exc, exc_info=True)
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": now,
        }
