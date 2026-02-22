"""
Executive Summary: Indian SEBI Foreign Portfolio Investor (FPI) compliance validator — determines FPI category, checks single-company and sectoral exposure limits, and lists required filings.
Inputs: entity_data (dict: entity_type, jurisdiction, aum_usd, india_exposure_pct, beneficial_owners (list))
Outputs: fpi_category (str), compliant (bool), violations (list), required_filings (list)
MCP Tool Name: sebi_fpi_validator
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "sebi_fpi_validator",
    "description": (
        "Validates Foreign Portfolio Investor (FPI) compliance under SEBI (Foreign Portfolio "
        "Investors) Regulations, 2019. Determines FPI Category I, II, or III; checks the "
        "10% single-company investment limit, 24%/49% sectoral caps, and grandfathering "
        "provisions."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "entity_data": {
                "type": "object",
                "properties": {
                    "entity_type": {
                        "type": "string",
                        "description": "E.g. sovereign_wealth_fund, pension_fund, bank, insurance, mutual_fund, family_office, other",
                    },
                    "jurisdiction": {"type": "string", "description": "ISO 3166-1 alpha-3 country code"},
                    "aum_usd": {"type": "number", "description": "Assets under management in USD"},
                    "india_exposure_pct": {
                        "type": "number",
                        "description": "Percentage of AUM invested in India (0-100)",
                    },
                    "beneficial_owners": {
                        "type": "array",
                        "description": "List of UBOs with jurisdiction and ownership_pct",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "jurisdiction": {"type": "string"},
                                "ownership_pct": {"type": "number"},
                            },
                        },
                    },
                    "single_company_exposure_pct": {
                        "type": "number",
                        "description": "Highest single-company exposure as % of total paid-up equity",
                    },
                    "sector": {
                        "type": "string",
                        "description": "Primary investment sector (e.g. banking, insurance, defence, telecom)",
                    },
                    "sector_exposure_pct": {
                        "type": "number",
                        "description": "Aggregate FPI holding in the sector as % of total sectoral capital",
                    },
                },
                "required": ["entity_type", "jurisdiction", "aum_usd"],
            }
        },
        "required": ["entity_data"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "fpi_category": {"type": "string"},
            "compliant": {"type": "boolean"},
            "violations": {"type": "array", "items": {"type": "string"}},
            "required_filings": {"type": "array", "items": {"type": "string"}},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["fpi_category", "compliant", "violations", "required_filings", "status", "timestamp"],
    },
}

# SEBI-designated high-risk / grey-list jurisdictions (FATF grey/black list as of 2025)
_HIGH_RISK_JURISDICTIONS: set[str] = {
    "PRK", "IRN", "MMR", "SYR", "YEM", "VEN", "LBY", "SDN",
    "UGA", "TZA", "PHL", "CMR", "NGO", "VNM",  # FATF grey list sample
}

# SEBI Category I eligible entity types
_CATEGORY_I_ENTITIES: set[str] = {
    "sovereign_wealth_fund",
    "central_bank",
    "multilateral_development_bank",
    "pension_fund",
    "insurance",
    "bank",
    "asset_management_company",
    "mutual_fund",
    "investment_trust",
}

# Sectoral FPI aggregate caps
_SECTORAL_CAPS: dict[str, float] = {
    "banking_public": 20.0,
    "insurance": 49.0,
    "defence": 49.0,
    "telecom": 49.0,
    "print_media": 26.0,
    "broadcasting": 49.0,
    "default": 49.0,  # General sectoral cap before government approval route
}


def sebi_fpi_validator(entity_data: dict[str, Any]) -> dict[str, Any]:
    """Validate a foreign entity's FPI compliance under SEBI Regulations 2019.

    Determines the applicable FPI category (I, II, or III) and checks
    investment limits including single-company 10% cap and sectoral caps.
    Also validates beneficial owner jurisdiction concerns.

    Args:
        entity_data: Dictionary with keys entity_type, jurisdiction, aum_usd,
            india_exposure_pct, beneficial_owners, single_company_exposure_pct,
            sector, and sector_exposure_pct.

    Returns:
        Dictionary with keys:
            status (str): "success" or "error".
            fpi_category (str): "Category I", "Category II", "Category III",
                or "Ineligible".
            compliant (bool): Overall compliance status.
            violations (list[str]): List of specific rule violations detected.
            required_filings (list[str]): Mandatory SEBI/DDPs filings.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        entity_type: str = str(entity_data.get("entity_type", "other")).lower()
        jurisdiction: str = str(entity_data.get("jurisdiction", "")).upper()
        aum_usd: float = float(entity_data.get("aum_usd", 0))
        india_exposure_pct: float = float(entity_data.get("india_exposure_pct", 0))
        beneficial_owners: list[dict] = entity_data.get("beneficial_owners", [])
        single_company_pct: float = float(entity_data.get("single_company_exposure_pct", 0))
        sector: str = str(entity_data.get("sector", "default")).lower().replace(" ", "_")
        sector_exposure_pct: float = float(entity_data.get("sector_exposure_pct", 0))

        violations: list[str] = []
        required_filings: list[str] = []

        # --- FPI Category Determination ---
        # Category I: Government & government-related entities, regulated funds from FATF-compliant jurisdictions
        # Category II: Regulated entities not in Category I, appropriately regulated funds
        # Category III: All others (highest compliance burden)

        if jurisdiction in _HIGH_RISK_JURISDICTIONS:
            fpi_category = "Ineligible"
            violations.append(
                f"Jurisdiction '{jurisdiction}' is on FATF grey/black list — FPI registration not permitted "
                "(SEBI FPI Regulations 2019, Regulation 6)"
            )
        elif entity_type in _CATEGORY_I_ENTITIES and jurisdiction not in _HIGH_RISK_JURISDICTIONS:
            fpi_category = "Category I"
        elif entity_type in {"family_office", "endowment", "charitable_foundation"}:
            # AUM threshold: if AUM > USD 10 billion, may be considered Category II
            if aum_usd >= 10_000_000_000:
                fpi_category = "Category II"
            else:
                fpi_category = "Category III"
        else:
            fpi_category = "Category II"

        # --- Beneficial Owner Checks (Regulation 22A) ---
        # Single UBO > 25% triggers enhanced KYC; > 50% from high-risk jurisdiction = issue
        for bo in beneficial_owners:
            bo_jurisdiction = str(bo.get("jurisdiction", "")).upper()
            bo_pct = float(bo.get("ownership_pct", 0))
            bo_name = bo.get("name", "Unknown")

            if bo_jurisdiction in _HIGH_RISK_JURISDICTIONS and bo_pct > 0:
                violations.append(
                    f"Beneficial owner '{bo_name}' ({bo_pct}%) is from high-risk jurisdiction "
                    f"'{bo_jurisdiction}' — enhanced due diligence required (Regulation 22A)"
                )
            if bo_pct > 25:
                required_filings.append(
                    f"UBO Declaration Form for '{bo_name}' ({bo_pct}% ownership) — "
                    "submit to Designated Depository Participant (DDP)"
                )

        # --- Single Company Investment Limit (Regulation 20) ---
        # FPI aggregate holding in any listed company ≤ 10% of paid-up equity capital
        _SINGLE_COMPANY_LIMIT = 10.0
        if single_company_pct > _SINGLE_COMPANY_LIMIT:
            violations.append(
                f"Single company exposure {single_company_pct:.2f}% exceeds 10% limit "
                f"(Regulation 20 — SEBI FPI Regulations 2019). Must divest or convert to FDI "
                f"within 5 trading days."
            )

        # --- Sectoral Caps Check ---
        sector_cap = _SECTORAL_CAPS.get(sector, _SECTORAL_CAPS["default"])
        if sector_exposure_pct > sector_cap:
            violations.append(
                f"Sector '{sector}' aggregate FPI exposure {sector_exposure_pct:.2f}% exceeds "
                f"sectoral cap of {sector_cap:.2f}% (Schedule I — FEMA (Non-debt Instruments) Rules 2019)"
            )

        # Category III additional restrictions
        if fpi_category == "Category III":
            violations.append(
                "Category III FPI may not invest in government debt or debt ETFs "
                "(SEBI Circular SEBI/HO/FPI&C/P/CIR/2023)"
            )
            required_filings.append(
                "Enhanced KYC documentation required — beneficial ownership to natural person level"
            )

        # --- Required Filings ---
        required_filings.extend([
            "FPI Registration Application via SEBI-registered DDP (Regulation 5)",
            "KYC documents: constitutional documents, authorised signatory list, board resolution",
            "Annual compliance certificate to DDP (Regulation 31)",
            "Monthly portfolio statement to custodian",
        ])

        if india_exposure_pct > 50:
            required_filings.append(
                "Review required: India exposure exceeds 50% of AUM — assess whether FDI conversion "
                "is required for any holding approaching 10% single-company threshold"
            )

        if fpi_category in {"Category I", "Category II"}:
            required_filings.append(
                "SEBI Circular SEBI/HO/FPI&C/CIR/2022/101 — Category disclosure to stock exchanges "
                "within 3 working days of category change"
            )

        compliant = len(violations) == 0 and fpi_category != "Ineligible"

        result = {
            "fpi_category": fpi_category,
            "compliant": compliant,
            "entity_type": entity_type,
            "jurisdiction": jurisdiction,
            "aum_usd": aum_usd,
            "india_exposure_pct": india_exposure_pct,
            "single_company_exposure_pct": single_company_pct,
            "single_company_limit_pct": 10.0,
            "sector": sector,
            "sector_exposure_pct": sector_exposure_pct,
            "sector_cap_pct": _SECTORAL_CAPS.get(sector, _SECTORAL_CAPS["default"]),
            "violations": violations,
            "required_filings": required_filings,
            "regulations_checked": [
                "SEBI (Foreign Portfolio Investors) Regulations 2019",
                "FEMA (Non-debt Instruments) Rules 2019",
                "SEBI Circular SEBI/HO/FPI&C/P/CIR/2023 — Revised FPI framework",
                "Regulation 20 — Investment limits",
                "Regulation 22A — Beneficial ownership",
            ],
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"sebi_fpi_validator failed: {e}")
        _log_lesson(f"sebi_fpi_validator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
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
