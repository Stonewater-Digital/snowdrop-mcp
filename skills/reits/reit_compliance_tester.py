"""Test REIT qualification rules."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "reit_compliance_tester",
    "description": "Evaluates income/asset/shareholder tests for REIT status.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "income_sources": {"type": "array", "items": {"type": "object"}},
            "assets": {"type": "array", "items": {"type": "object"}},
            "distributions": {"type": "object"},
            "shareholders": {"type": "object"},
        },
        "required": ["income_sources", "assets", "distributions", "shareholders"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def reit_compliance_tester(
    income_sources: list[dict[str, Any]],
    assets: list[dict[str, Any]],
    distributions: dict[str, Any],
    shareholders: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Return REIT compliance status."""
    try:
        income_total = sum(i.get("amount", 0.0) for i in income_sources)
        test75 = sum(i.get("amount", 0.0) for i in income_sources if i.get("qualifies_75_pct_test")) / income_total * 100 if income_total else 0.0
        test95 = sum(i.get("amount", 0.0) for i in income_sources if i.get("qualifies_95_pct_test")) / income_total * 100 if income_total else 0.0
        asset_total = sum(a.get("value", 0.0) for a in assets)
        asset_qual = sum(a.get("value", 0.0) for a in assets if a.get("is_real_estate") or a.get("is_cash") or a.get("is_government_securities")) / asset_total * 100 if asset_total else 0.0
        distribution_req = distributions.get("dividends_paid", 0.0) >= 0.9 * distributions.get("taxable_income", 0.0)
        shareholder_test = shareholders.get("count", 0) >= 100 and shareholders.get("top_5_ownership_pct", 0.0) <= 50
        tests = [
            {"test": "75% income", "result": test75, "passing": test75 >= 75},
            {"test": "95% income", "result": test95, "passing": test95 >= 95},
            {"test": "75% assets", "result": asset_qual, "passing": asset_qual >= 75},
            {"test": "Distribution", "result": distribution_req, "passing": distribution_req},
            {"test": "100 shareholders", "result": shareholders.get("count", 0), "passing": shareholders.get("count", 0) >= 100},
            {"test": "5/50", "result": shareholders.get("top_5_ownership_pct", 0.0), "passing": shareholder_test},
        ]
        headroom = {
            "75_income": round(test75 - 75, 2),
            "95_income": round(test95 - 95, 2),
            "75_assets": round(asset_qual - 75, 2),
        }
        failing = [t for t in tests if not t["passing"]]
        data = {
            "qualified": not failing,
            "tests": tests,
            "closest_to_failure": min(tests, key=lambda t: t["result"] - (75 if "75" in t["test"] else 0)) if tests else None,
            "headroom_by_test": headroom,
            "remediation_needed": [t["test"] for t in failing],
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("reit_compliance_tester", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
