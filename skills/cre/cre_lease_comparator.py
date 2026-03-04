"""Compare lease structures (NNN vs gross)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "cre_lease_comparator",
    "description": "Evaluates tenant/landlord economics for NNN, gross, and modified gross leases.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "base_rent_psf": {"type": "number"},
            "rentable_sqft": {"type": "integer"},
            "opex_psf": {"type": "number"},
            "cam_psf": {"type": "number"},
            "insurance_psf": {"type": "number"},
            "tax_psf": {"type": "number"},
            "annual_escalation_pct": {"type": "number"},
            "lease_term_years": {"type": "integer"},
            "ti_allowance_psf": {"type": "number"},
            "free_rent_months": {"type": "integer"},
        },
        "required": [
            "base_rent_psf",
            "rentable_sqft",
            "opex_psf",
            "cam_psf",
            "insurance_psf",
            "tax_psf",
            "annual_escalation_pct",
            "lease_term_years",
            "ti_allowance_psf",
            "free_rent_months",
        ],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def cre_lease_comparator(
    base_rent_psf: float,
    rentable_sqft: int,
    opex_psf: float,
    cam_psf: float,
    insurance_psf: float,
    tax_psf: float,
    annual_escalation_pct: float,
    lease_term_years: int,
    ti_allowance_psf: float,
    free_rent_months: int,
    **_: Any,
) -> dict[str, Any]:
    """Return lease economics for different structures."""
    try:
        rent = base_rent_psf * rentable_sqft
        opex = (opex_psf + cam_psf + insurance_psf + tax_psf) * rentable_sqft
        escalation = 1 + annual_escalation_pct / 100
        effective_months = lease_term_years * 12 - free_rent_months
        ti_total = ti_allowance_psf * rentable_sqft
        def _effective_rent(structure: str) -> float:
            cash_flows = []
            annual_rent = rent
            for year in range(lease_term_years):
                payment = annual_rent
                if structure == "gross":
                    payment -= opex
                elif structure == "modified_gross":
                    payment -= opex * 0.5
                cash_flows.append(payment)
                annual_rent *= escalation
            total = sum(cash_flows) - ti_total
            return total / effective_months
        nnn = {
            "effective_rent_psf": round(_effective_rent("nnn") / rentable_sqft * 12, 2),
            "landlord_noi": round(rent - ti_total / lease_term_years, 2),
        }
        gross = {
            "effective_rent_psf": round(_effective_rent("gross") / rentable_sqft * 12, 2),
            "landlord_noi": round(rent - opex - ti_total / lease_term_years, 2),
        }
        modified = {
            "effective_rent_psf": round(_effective_rent("modified_gross") / rentable_sqft * 12, 2),
            "landlord_noi": round(rent - opex * 0.5 - ti_total / lease_term_years, 2),
        }
        landlord_best = max((nnn, "nnn"), (gross, "gross"), (modified, "modified_gross"), key=lambda x: x[0]["landlord_noi"])[1]
        tenant_best = min((nnn, "nnn"), (gross, "gross"), (modified, "modified_gross"), key=lambda x: x[0]["effective_rent_psf"])[1]
        data = {
            "nnn": nnn,
            "gross": gross,
            "modified_gross": modified,
            "landlord_best": landlord_best,
            "tenant_best": tenant_best,
            "effective_rent_comparison": {"nnn": nnn["effective_rent_psf"], "gross": gross["effective_rent_psf"], "modified": modified["effective_rent_psf"]},
            "npv_comparison": {"nnn": round(nnn["landlord_noi"], 2), "gross": round(gross["landlord_noi"], 2), "modified": round(modified["landlord_noi"], 2)},
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("cre_lease_comparator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
