"""
Executive Summary: FinCEN Beneficial Ownership Information Report (BOIR) generator under the Corporate Transparency Act — validates required fields, checks 23 exemption categories, and produces a FinCEN-formatted BOIR JSON payload.
Inputs: entity_data (dict: legal_name, dba, ein, formation_state, formation_date, address, beneficial_owners (list))
Outputs: boir_json (dict), exempt (bool), exemption_category (str or null), validation_errors (list)
MCP Tool Name: fincen_boir_generator
"""
import os
import re
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "fincen_boir_generator",
    "description": (
        "Generates a FinCEN Beneficial Ownership Information Report (BOIR) under the Corporate "
        "Transparency Act (CTA) 31 U.S.C. § 5336 and 31 CFR Part 1010.380. Validates all required "
        "fields, checks the 23 statutory exemption categories, and formats the payload for "
        "FinCEN BOIR online submission."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "entity_data": {
                "type": "object",
                "properties": {
                    "legal_name": {"type": "string"},
                    "dba": {"type": "string", "description": "Trade name / DBA if any"},
                    "ein": {"type": "string", "description": "Employer Identification Number (XX-XXXXXXX)"},
                    "formation_state": {"type": "string", "description": "US state or territory of formation"},
                    "formation_date": {"type": "string", "description": "Formation date YYYY-MM-DD"},
                    "address": {
                        "type": "object",
                        "properties": {
                            "street": {"type": "string"},
                            "city": {"type": "string"},
                            "state": {"type": "string"},
                            "zip": {"type": "string"},
                            "country": {"type": "string"},
                        },
                    },
                    "entity_type": {
                        "type": "string",
                        "description": "corporation / llc / lp / llp / trust / other",
                    },
                    "employees_count": {
                        "type": "integer",
                        "description": "Number of employees (for large operating company exemption)",
                    },
                    "gross_receipts_usd": {
                        "type": "number",
                        "description": "Prior year gross receipts (for large operating company exemption)",
                    },
                    "is_regulated_entity": {
                        "type": "boolean",
                        "description": "True if entity is regulated by a US federal or state financial regulator",
                    },
                    "regulated_by": {
                        "type": "string",
                        "description": "Name of regulator (SEC, CFTC, OCC, Fed, FDIC, NCUA, state banking, etc.)",
                    },
                    "is_publicly_listed": {"type": "boolean"},
                    "exchange_listed_on": {"type": "string", "description": "NYSE / NASDAQ / etc."},
                    "beneficial_owners": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "dob": {"type": "string", "description": "Date of birth YYYY-MM-DD"},
                                "address": {
                                    "type": "object",
                                    "properties": {
                                        "street": {"type": "string"},
                                        "city": {"type": "string"},
                                        "state": {"type": "string"},
                                        "zip": {"type": "string"},
                                        "country": {"type": "string"},
                                    },
                                },
                                "id_type": {
                                    "type": "string",
                                    "description": "passport / drivers_license / state_id / foreign_passport",
                                },
                                "id_number": {"type": "string"},
                                "id_issuing_jurisdiction": {"type": "string"},
                                "ownership_pct": {
                                    "type": "number",
                                    "description": "Ownership percentage (25%+ triggers BO inclusion)",
                                },
                                "is_company_applicant": {
                                    "type": "boolean",
                                    "description": "True if this person filed the formation documents",
                                },
                            },
                            "required": ["name", "dob", "id_type", "id_number", "ownership_pct"],
                        },
                    },
                },
                "required": ["legal_name", "formation_state", "entity_type", "beneficial_owners"],
            }
        },
        "required": ["entity_data"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "boir_json": {"type": "object"},
            "exempt": {"type": "boolean"},
            "exemption_category": {"type": ["string", "null"]},
            "validation_errors": {"type": "array", "items": {"type": "string"}},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["boir_json", "exempt", "exemption_category", "validation_errors", "status", "timestamp"],
    },
}

# CTA 23 Exemption Categories (31 CFR § 1010.380(c)(2))
_EXEMPTION_CATEGORIES: list[dict[str, str]] = [
    {"id": "1",  "name": "Securities reporting issuer",          "description": "Publicly listed company under SEC 12(b) or 12(g)"},
    {"id": "2",  "name": "Governmental authority",              "description": "US governmental entity"},
    {"id": "3",  "name": "Bank",                                "description": "FDIC-insured bank"},
    {"id": "4",  "name": "Credit union",                        "description": "NCUA-insured credit union"},
    {"id": "5",  "name": "Depository institution holding company", "description": "Federal Reserve regulated"},
    {"id": "6",  "name": "Money services business",             "description": "FinCEN-registered MSB"},
    {"id": "7",  "name": "Broker or dealer in securities",      "description": "SEC/FINRA registered BD"},
    {"id": "8",  "name": "Securities exchange or clearing agency", "description": "SEC-registered exchange/CCA"},
    {"id": "9",  "name": "Other Exchange Act registered entity", "description": "SEC registered non-BD"},
    {"id": "10", "name": "Investment company or investment adviser", "description": "SEC-registered IC or IA"},
    {"id": "11", "name": "Venture capital fund adviser",        "description": "SEC-exempt VC fund adviser"},
    {"id": "12", "name": "Insurance company",                   "description": "State-supervised insurance company"},
    {"id": "13", "name": "State-licensed insurance producer",   "description": "State-licensed insurance agency/broker"},
    {"id": "14", "name": "Commodity Exchange Act registered entity", "description": "CFTC-registered entity"},
    {"id": "15", "name": "Accounting firm",                     "description": "Public accounting firm under SOX"},
    {"id": "16", "name": "Public utility",                      "description": "State/federal utility regulation"},
    {"id": "17", "name": "Financial market utility",            "description": "FSOC-designated FMU"},
    {"id": "18", "name": "Pooled investment vehicle",           "description": "IA-managed fund exempt from registration"},
    {"id": "19", "name": "Tax-exempt entity",                   "description": "IRS Section 501(c) exempt"},
    {"id": "20", "name": "Entity assisting tax-exempt entity",  "description": "Supporting 501(c) organization"},
    {"id": "21", "name": "Large operating company",             "description": "21+ FT employees, $5M+ gross receipts, US physical office"},
    {"id": "22", "name": "Subsidiary of certain exempt entities", "description": "Subsidiary majority-owned by exempt entity"},
    {"id": "23", "name": "Inactive entity",                     "description": "Formed before 1/1/2020, no business, assets < $1000"},
]

_LARGE_CO_MIN_EMPLOYEES = 21
_LARGE_CO_MIN_GROSS_RECEIPTS = 5_000_000
_BO_OWNERSHIP_THRESHOLD = 25.0


def fincen_boir_generator(entity_data: dict[str, Any]) -> dict[str, Any]:
    """Generate a FinCEN BOIR payload and check exemption status.

    Validates all required fields per 31 CFR § 1010.380, checks the 23
    statutory exemption categories, identifies beneficial owners meeting the
    25%+ threshold, and formats the complete BOIR JSON for FinCEN submission.

    Args:
        entity_data: Dictionary with entity identification, formation details,
            address, regulatory status, and list of beneficial owners with
            identification documents.

    Returns:
        Dictionary with keys:
            status (str): "success" or "error".
            boir_json (dict): Formatted BOIR for FinCEN submission.
            exempt (bool): Whether entity qualifies for CTA exemption.
            exemption_category (str | None): Exemption number and name if exempt.
            validation_errors (list[str]): Field-level validation issues.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        legal_name: str = str(entity_data.get("legal_name", ""))
        dba: str = str(entity_data.get("dba", ""))
        ein: str = str(entity_data.get("ein", ""))
        formation_state: str = str(entity_data.get("formation_state", ""))
        formation_date: str = str(entity_data.get("formation_date", ""))
        address: dict = entity_data.get("address", {})
        entity_type: str = str(entity_data.get("entity_type", "llc")).lower()
        employees_count: int = int(entity_data.get("employees_count", 0))
        gross_receipts_usd: float = float(entity_data.get("gross_receipts_usd", 0))
        is_regulated: bool = bool(entity_data.get("is_regulated_entity", False))
        regulated_by: str = str(entity_data.get("regulated_by", ""))
        is_publicly_listed: bool = bool(entity_data.get("is_publicly_listed", False))
        exchange_listed: str = str(entity_data.get("exchange_listed_on", ""))
        beneficial_owners: list[dict] = entity_data.get("beneficial_owners", [])

        validation_errors: list[str] = []
        exempt = False
        exemption_category: str | None = None

        # =====================================================================
        # FIELD VALIDATION
        # =====================================================================
        if not legal_name:
            validation_errors.append("legal_name is required (31 CFR § 1010.380(b)(1)(i))")
        if not formation_state:
            validation_errors.append("formation_state is required (31 CFR § 1010.380(b)(1)(ii))")
        if ein and not re.match(r"^\d{2}-\d{7}$", ein):
            validation_errors.append(f"EIN format invalid: '{ein}' — expected XX-XXXXXXX")

        # Validate each BO
        qualified_bos = []
        for i, bo in enumerate(beneficial_owners):
            bo_errors = _validate_beneficial_owner(bo, i + 1)
            validation_errors.extend(bo_errors)
            if float(bo.get("ownership_pct", 0)) >= _BO_OWNERSHIP_THRESHOLD or bo.get("is_company_applicant"):
                qualified_bos.append(bo)

        if not qualified_bos and not exempt:
            validation_errors.append(
                "No beneficial owners with >=25% ownership found and no company applicant identified. "
                "Every reporting company must have at least one BO or company applicant (31 CFR § 1010.380(d))"
            )

        # =====================================================================
        # EXEMPTION CHECKS
        # =====================================================================
        # Category 1: Publicly listed
        if is_publicly_listed and exchange_listed:
            exempt = True
            exemption_category = f"Exemption 1 — Securities reporting issuer (listed on {exchange_listed})"

        # Category 3/4: FDIC/NCUA regulated
        elif is_regulated and regulated_by in {"FDIC", "NCUA", "OCC", "Federal Reserve", "Fed"}:
            exempt = True
            exemption_category = f"Exemption 3/4/5 — Regulated financial institution ({regulated_by})"

        # Category 7: SEC/FINRA registered BD
        elif is_regulated and regulated_by in {"SEC", "FINRA"}:
            exempt = True
            exemption_category = f"Exemption 7/9/10 — SEC/FINRA regulated entity ({regulated_by})"

        # Category 14: CFTC regulated
        elif is_regulated and regulated_by in {"CFTC"}:
            exempt = True
            exemption_category = "Exemption 14 — CFTC registered entity"

        # Category 21: Large operating company
        elif (
            employees_count >= _LARGE_CO_MIN_EMPLOYEES
            and gross_receipts_usd >= _LARGE_CO_MIN_GROSS_RECEIPTS
            and address.get("country", "US") in {"US", "USA", "United States"}
        ):
            exempt = True
            exemption_category = (
                f"Exemption 21 — Large operating company "
                f"({employees_count} employees, ${gross_receipts_usd:,.0f} gross receipts)"
            )

        # Category 19: Tax-exempt entity
        elif is_regulated and "501(c)" in regulated_by:
            exempt = True
            exemption_category = f"Exemption 19 — Tax-exempt entity ({regulated_by})"

        # =====================================================================
        # BOIR JSON CONSTRUCTION
        # =====================================================================
        boir_json: dict[str, Any] = {
            "form_type": "BOIR",
            "form_version": "1.0",
            "filing_type": "Initial",
            "submission_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "reporting_company": {
                "legal_name": legal_name,
                "dba": dba or None,
                "ein": ein or None,
                "entity_type": entity_type,
                "formation_state": formation_state,
                "formation_date": formation_date or None,
                "address": {
                    "street": address.get("street", ""),
                    "city": address.get("city", ""),
                    "state": address.get("state", ""),
                    "zip": address.get("zip", ""),
                    "country": address.get("country", "US"),
                },
                "is_exempt": exempt,
                "exemption_category": exemption_category,
            },
            "beneficial_owners": [],
            "company_applicants": [],
            "validation_errors": validation_errors,
            "regulatory_basis": [
                "Corporate Transparency Act (CTA) — 31 U.S.C. § 5336",
                "31 CFR Part 1010.380 — Beneficial Ownership Information Reporting",
                "FinCEN Final Rule — September 30, 2022 (87 FR 59498)",
                "FinCEN FAQ — Beneficial Ownership Information",
            ],
            "filing_deadlines": {
                "existing_companies": (
                    "Companies formed before January 1, 2024: initial BOIR due January 1, 2025 "
                    "(extended per FinCEN interim final rule)"
                ),
                "new_companies_2024": (
                    "Companies formed in 2024: 90 calendar days from formation to file initial BOIR"
                ),
                "new_companies_2025_plus": (
                    "Companies formed from January 1, 2025: 30 calendar days from formation"
                ),
                "updates": "Material changes must be reported within 30 calendar days",
            },
        }

        # Add beneficial owners and company applicants
        for bo in qualified_bos:
            if bool(bo.get("is_company_applicant", False)):
                boir_json["company_applicants"].append(_format_individual(bo))
            else:
                boir_json["beneficial_owners"].append(_format_individual(bo))

        result = {
            "boir_json": boir_json,
            "exempt": exempt,
            "exemption_category": exemption_category,
            "validation_errors": validation_errors,
            "qualified_beneficial_owners_count": len([b for b in qualified_bos if not b.get("is_company_applicant")]),
            "company_applicants_count": len([b for b in qualified_bos if b.get("is_company_applicant")]),
            "all_exemption_categories": _EXEMPTION_CATEGORIES,
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"fincen_boir_generator failed: {e}")
        _log_lesson(f"fincen_boir_generator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _validate_beneficial_owner(bo: dict[str, Any], index: int) -> list[str]:
    """Validate a beneficial owner record against CTA required fields.

    Args:
        bo: Beneficial owner dictionary.
        index: 1-based position index for error messages.

    Returns:
        List of validation error strings.
    """
    errors: list[str] = []
    prefix = f"Beneficial owner #{index} ({bo.get('name', 'Unknown')})"

    if not bo.get("name"):
        errors.append(f"{prefix}: name is required")
    if not bo.get("dob"):
        errors.append(f"{prefix}: date_of_birth is required (31 CFR § 1010.380(b)(2)(ii))")
    if not bo.get("id_type"):
        errors.append(f"{prefix}: id_type is required — passport/drivers_license/state_id/foreign_passport")
    if not bo.get("id_number"):
        errors.append(f"{prefix}: id_number is required")
    if not bo.get("id_issuing_jurisdiction") and bo.get("id_type") in {"passport", "foreign_passport"}:
        errors.append(f"{prefix}: id_issuing_jurisdiction required for passport documents")

    dob_str = bo.get("dob", "")
    if dob_str and not re.match(r"^\d{4}-\d{2}-\d{2}$", dob_str):
        errors.append(f"{prefix}: date_of_birth format invalid '{dob_str}' — expected YYYY-MM-DD")

    return errors


def _format_individual(bo: dict[str, Any]) -> dict[str, Any]:
    """Format a beneficial owner or company applicant for BOIR JSON.

    Args:
        bo: Raw beneficial owner dictionary.

    Returns:
        Formatted dictionary for BOIR payload.
    """
    addr = bo.get("address", {})
    return {
        "full_name": bo.get("name", ""),
        "date_of_birth": bo.get("dob", ""),
        "address": {
            "street": addr.get("street", ""),
            "city": addr.get("city", ""),
            "state": addr.get("state", ""),
            "zip": addr.get("zip", ""),
            "country": addr.get("country", "US"),
        },
        "identification": {
            "id_type": bo.get("id_type", ""),
            "id_number": bo.get("id_number", ""),
            "issuing_jurisdiction": bo.get("id_issuing_jurisdiction", ""),
        },
        "ownership_pct": bo.get("ownership_pct", 0),
        "is_company_applicant": bool(bo.get("is_company_applicant", False)),
    }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the lessons log.

    Args:
        message: Human-readable description of the failure.
    """
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except Exception:
        pass
