"""Benchmark token efficiency across contribution sources."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "token_efficiency_benchmarker",
    "description": "Compares tokens per skill/line/quality across internal and community contributors.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "contributions": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["contributions"],
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


def token_efficiency_benchmarker(contributions: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return efficiency metrics per source and strategic guidance."""
    try:
        if not contributions:
            raise ValueError("contributions required")
        rows = []
        for entry in contributions:
            source = entry.get("source")
            tokens = entry.get("tokens_input", 0)
            skills = entry.get("skills_produced", 0)
            lines = entry.get("lines_produced", 0)
            quality = entry.get("quality_score", 1)
            price_per_token = 0.0005 if "community" in source else 0.001
            cost = tokens * price_per_token
            rows.append(
                {
                    "source": source,
                    "tokens_per_skill": tokens / max(skills, 1),
                    "tokens_per_line": tokens / max(lines, 1),
                    "quality_adjusted_efficiency": tokens / max(quality, 0.1),
                    "cost_per_skill": cost / max(skills, 1),
                }
            )
        most = min(rows, key=lambda r: r["tokens_per_skill"])["source"]
        least = max(rows, key=lambda r: r["tokens_per_skill"])["source"]
        codex_vs_claude = _ratio(rows, "internal_codex", "community_sonnet")
        community_vs_internal = _ratio_group(rows, "community", "internal")
        strategy = "Lean into community" if community_vs_internal < 1 else "Blend with internal"
        data = {
            "efficiency_by_source": rows,
            "most_efficient": most,
            "least_efficient": least,
            "codex_vs_claude_ratio": round(codex_vs_claude, 2) if codex_vs_claude else None,
            "community_vs_internal_efficiency": round(community_vs_internal, 2) if community_vs_internal else None,
            "optimal_strategy": strategy,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("token_efficiency_benchmarker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _ratio(rows: list[dict[str, Any]], num: str, den: str) -> float | None:
    lookup = {row["source"]: row for row in rows}
    if num not in lookup or den not in lookup:
        return None
    return lookup[num]["tokens_per_skill"] / max(lookup[den]["tokens_per_skill"], 1e-6)


def _ratio_group(rows: list[dict[str, Any]], a: str, b: str) -> float | None:
    group_a = [r for r in rows if a in r["source"]]
    group_b = [r for r in rows if b in r["source"]]
    if not group_a or not group_b:
        return None
    avg_a = sum(r["tokens_per_skill"] for r in group_a) / len(group_a)
    avg_b = sum(r["tokens_per_skill"] for r in group_b) / len(group_b)
    return avg_a / max(avg_b, 1e-6)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
