"""Generate investor pitch deck outlines."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "pitch_deck_generator",
    "description": "Creates slide-by-slide pitch content for Snowdrop fundraising narratives.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "company": {"type": "object"},
            "financials": {"type": "object"},
            "market": {"type": "object"},
            "traction": {"type": "object"},
            "ask": {"type": "object"},
        },
        "required": ["company", "financials", "market", "traction", "ask"],
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


_SECTIONS = [
    "Problem",
    "Solution",
    "Market Size",
    "Traction",
    "Business Model",
    "Financials",
    "Team",
    "Ask",
]


def pitch_deck_generator(
    company: dict[str, Any],
    financials: dict[str, Any],
    market: dict[str, Any],
    traction: dict[str, Any],
    ask: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Return slide outlines for an investor pitch deck."""
    try:
        slides = []
        for section in _SECTIONS:
            slides.append(_build_slide(section, company, financials, market, traction, ask))
        data = {"slides": slides}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("pitch_deck_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _build_slide(
    section: str,
    company: dict[str, Any],
    financials: dict[str, Any],
    market: dict[str, Any],
    traction: dict[str, Any],
    ask: dict[str, Any],
) -> dict[str, Any]:
    bullets: list[str] = []
    notes = ""
    if section == "Problem":
        bullets = [
            "Agents lack unified treasury automation",
            "Legacy stacks ignore multi-chain reconciliation",
        ]
        notes = "Quantify pain via customer anecdotes."
    elif section == "Solution":
        bullets = [
            f"{company.get('name')} deploys Sovereign Financial Intelligence",
            "Human-on-the-loop ensures trust + automation",
        ]
        notes = company.get("mission", "")
    elif section == "Market Size":
        bullets = [
            f"TAM: ${market.get('tam', 'N/A')}B",
            f"SAM: ${market.get('sam', 'N/A')}B",
            f"SOM: ${market.get('som', 'N/A')}B",
        ]
        notes = "Highlight fastest-growing segments"
    elif section == "Traction":
        bullets = [
            f"Agents onboarded: {traction.get('agents_count', 0)}",
            f"Skills live: {traction.get('skills_count', 0)}",
            f"Revenue to-date: ${traction.get('revenue_to_date', 0)}",
        ]
        notes = "Include logo garden"
    elif section == "Business Model":
        bullets = ["Usage-based Skill fees", "LP/GP services", "Treasury automation"]
        notes = "Show unit economics"
    elif section == "Financials":
        bullets = [
            f"MRR: ${financials.get('mrr', 0)}",
            f"Growth: {financials.get('growth_rate', 0)}% MoM",
            f"Runway: {financials.get('runway_months', 0)} months",
        ]
        notes = "Add burn multiple"
    elif section == "Team":
        bullets = ["Thunder Peters — Operator", "Snowdrop Swarm — multi-model bench"]
        notes = "Add advisors"
    elif section == "Ask":
        bullets = [
            f"Raising ${ask.get('amount', 'N/A')} to scale",
            "Use of funds: " + ", ".join(f"{item.get('category')}: {item.get('percentage')}%" for item in ask.get("use_of_funds", [])),
        ]
        notes = "State milestones"
    return {"title": section, "bullets": bullets, "notes": notes}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
