"""Compute Piotroski F-Scores for equity strength."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "piotroski_f_score",
    "description": "Evaluates the nine Piotroski signals to rate financial strength.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current": {"type": "object"},
            "prior": {"type": "object"},
        },
        "required": ["current", "prior"],
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


def piotroski_f_score(current: dict[str, Any], prior: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Return F-score breakdown and classification."""
    try:
        tests = []
        score = 0
        def add_test(name: str, passed: bool, signal: str) -> None:
            nonlocal score
            score += int(passed)
            tests.append({"test": name, "passed": passed, "signal": signal})

        add_test("Positive ROA", current.get("roa", 0) > 0, "profitability")
        add_test("Positive OCF", current.get("operating_cf", 0) > 0, "cash_flow")
        add_test("ROA improving", current.get("roa", 0) > prior.get("roa", 0), "trend")
        add_test("Accruals", current.get("operating_cf", 0) > current.get("net_income", 0), "quality")
        add_test(
            "Lower leverage",
            current.get("long_term_debt", 0) < prior.get("long_term_debt", 0),
            "leverage",
        )
        add_test(
            "Higher liquidity",
            current.get("current_ratio", 0) > prior.get("current_ratio", 0),
            "liquidity",
        )
        add_test(
            "No dilution",
            current.get("shares_outstanding", 0) <= prior.get("shares_outstanding", 0),
            "structure",
        )
        add_test(
            "Gross margin improving",
            current.get("gross_margin", 0) > prior.get("gross_margin", 0),
            "margin",
        )
        add_test(
            "Asset turnover improving",
            current.get("asset_turnover", 0) > prior.get("asset_turnover", 0),
            "efficiency",
        )
        strength = "neutral"
        if score >= 8:
            strength = "strong"
        elif score <= 2:
            strength = "weak"
        signals = [t["test"] for t in tests if not t["passed"]]
        data = {
            "f_score": score,
            "max_score": 9,
            "tests": tests,
            "strength": strength,
            "signals": signals,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("piotroski_f_score", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
