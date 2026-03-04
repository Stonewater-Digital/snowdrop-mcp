"""Test NMTC project compliance."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "nmtc_compliance_checker",
    "description": "Evaluates census tract, QALICB, and substantially-all tests for NMTC projects.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "project": {"type": "object"},
            "qlici": {"type": "object"},
            "substantially_all_test": {"type": "object"},
        },
        "required": ["project", "qlici", "substantially_all_test"],
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


def nmtc_compliance_checker(
    project: dict[str, Any],
    qlici: dict[str, Any],
    substantially_all_test: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Return NMTC compliance status and risks."""
    try:
        tract_ok = project.get("tract_poverty_rate", 0.0) >= 20 or project.get("tract_median_income_pct", 100) <= 80
        business_type = project.get("business_type", "")
        sin_business = business_type in {"casino", "golf", "liquor", "tanning"}
        substantially_all_pct = substantially_all_test.get("pct_in_low_income", 0.0)
        substantially_all_met = substantially_all_pct >= 85
        tests = [
            {"name": "Census tract", "passing": tract_ok},
            {"name": "QALICB restriction", "passing": not sin_business},
            {"name": "Substantially all", "passing": substantially_all_met},
        ]
        recapture_risks = []
        if not tract_ok:
            recapture_risks.append("Tract fails poverty/median income thresholds")
        if sin_business:
            recapture_risks.append("Prohibited business type")
        if not substantially_all_met:
            recapture_risks.append("Substantially-all test shortfall")
        data = {
            "eligible": not recapture_risks,
            "tests": tests,
            "census_tract_qualified": tract_ok,
            "substantially_all_met": substantially_all_met,
            "recapture_risks": recapture_risks,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("nmtc_compliance_checker", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
