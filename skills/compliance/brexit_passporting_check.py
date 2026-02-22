"""
Executive Summary: Post-Brexit UK-EU cross-border financial services licensing checker — confirms passporting is unavailable, identifies required local licences per target market, and evaluates equivalence decisions.
Inputs: entity_data (dict: registered_jurisdiction, target_markets, license_type, has_uk_branch, has_eu_branch)
Outputs: passporting_available (bool), required_licenses (list of dicts), equivalence_status (dict), recommendations (list)
MCP Tool Name: brexit_passporting_check
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "brexit_passporting_check",
    "description": (
        "Post-Brexit cross-border licensing analysis for UK and EU financial services. "
        "Confirms that EEA passporting is definitively unavailable since 31 December 2020, "
        "evaluates available equivalence decisions, and determines local authorisation "
        "requirements per target market and licence type."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "entity_data": {
                "type": "object",
                "properties": {
                    "registered_jurisdiction": {
                        "type": "string",
                        "description": "Where the firm is currently authorised (e.g. 'GB', 'IE', 'DE', 'FR')",
                    },
                    "target_markets": {
                        "type": "array",
                        "description": "ISO 3166-1 alpha-2 country codes of markets to access",
                        "items": {"type": "string"},
                    },
                    "license_type": {
                        "type": "string",
                        "description": "Type of financial service licence: investment_firm / credit_institution / payment_institution / e_money / fund_manager / insurance",
                    },
                    "has_uk_branch": {"type": "boolean"},
                    "has_eu_branch": {"type": "boolean"},
                    "is_third_country_firm": {
                        "type": "boolean",
                        "description": "True if firm is authorised outside both UK and EEA",
                    },
                },
                "required": ["registered_jurisdiction", "target_markets", "license_type"],
            }
        },
        "required": ["entity_data"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "passporting_available": {"type": "boolean"},
            "required_licenses": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "market": {"type": "string"},
                        "license_type": {"type": "string"},
                        "authority": {"type": "string"},
                    },
                },
            },
            "equivalence_status": {"type": "object"},
            "recommendations": {"type": "array", "items": {"type": "string"}},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": [
            "passporting_available",
            "required_licenses",
            "equivalence_status",
            "recommendations",
            "status",
            "timestamp",
        ],
    },
}

# EU member states (EEA)
_EU_EEA_COUNTRIES: set[str] = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR",
    "DE", "GR", "HU", "IS", "IE", "IT", "LV", "LI", "LT", "LU",
    "MT", "NL", "NO", "PL", "PT", "RO", "SK", "SI", "ES", "SE",
}

# National competent authorities by country
_COMPETENT_AUTHORITIES: dict[str, dict[str, str]] = {
    "GB": {"investment_firm": "FCA", "credit_institution": "PRA/FCA", "payment_institution": "FCA",
           "e_money": "FCA", "fund_manager": "FCA", "insurance": "PRA"},
    "IE": {"investment_firm": "CBI", "credit_institution": "CBI", "payment_institution": "CBI",
           "e_money": "CBI", "fund_manager": "CBI", "insurance": "CBI"},
    "DE": {"investment_firm": "BaFin", "credit_institution": "BaFin", "payment_institution": "BaFin",
           "e_money": "BaFin", "fund_manager": "BaFin", "insurance": "BaFin"},
    "FR": {"investment_firm": "AMF/ACPR", "credit_institution": "ACPR", "payment_institution": "ACPR",
           "e_money": "ACPR", "fund_manager": "AMF", "insurance": "ACPR"},
    "LU": {"investment_firm": "CSSF", "credit_institution": "CSSF", "payment_institution": "CSSF",
           "e_money": "CSSF", "fund_manager": "CSSF", "insurance": "CAA"},
    "NL": {"investment_firm": "AFM", "credit_institution": "DNB", "payment_institution": "DNB",
           "e_money": "DNB", "fund_manager": "AFM", "insurance": "DNB"},
    "ES": {"investment_firm": "CNMV", "credit_institution": "BdE", "payment_institution": "BdE",
           "e_money": "BdE", "fund_manager": "CNMV", "insurance": "DGSFP"},
    "IT": {"investment_firm": "CONSOB/Banca d'Italia", "credit_institution": "Banca d'Italia",
           "payment_institution": "Banca d'Italia", "e_money": "Banca d'Italia",
           "fund_manager": "Banca d'Italia", "insurance": "IVASS"},
    "SE": {"investment_firm": "Finansinspektionen", "credit_institution": "Finansinspektionen",
           "payment_institution": "Finansinspektionen", "e_money": "Finansinspektionen",
           "fund_manager": "Finansinspektionen", "insurance": "Finansinspektionen"},
}

# Equivalence decisions granted by EU to UK (as of 2025 — very limited)
# EU has granted minimal equivalence to UK post-Brexit
_EU_UK_EQUIVALENCE: dict[str, dict[str, Any]] = {
    "CCPs": {
        "granted": True,
        "scope": "Central counterparty recognition under EMIR Art. 25",
        "expiry": "2025-06-30",
        "notes": "Temporary equivalence for UK CCPs (LCH, ICE Clear Europe) extended multiple times",
    },
    "CSDs": {
        "granted": False,
        "scope": "Central securities depositories",
        "notes": "No equivalence granted — UK CSDs not recognised for EU settlement",
    },
    "investment_firms_mifid": {
        "granted": False,
        "scope": "Investment firms — MiFID II Third Country access",
        "notes": (
            "No equivalence granted for UK investment firms under MiFIR Art. 47. "
            "UK firms must use local branches or reverse solicitation only."
        ),
    },
    "credit_institutions": {
        "granted": False,
        "scope": "Banking / credit institution passporting",
        "notes": "No equivalence — UK banks require local authorisation in each EU member state",
    },
    "fund_managers_aifmd": {
        "granted": False,
        "scope": "Alternative fund managers — AIFMD third-country passport",
        "notes": "AIFMD third-country passport not yet activated by ESMA for UK managers",
    },
    "insurance_solvency_ii": {
        "granted": False,
        "scope": "Insurance undertakings — Solvency II equivalence",
        "notes": "Partial: UK recognised as equivalent for reinsurance (Art. 172) and group supervision (Art. 227)",
    },
}

# UK equivalence decisions for EU (post-Brexit)
_UK_EU_EQUIVALENCE: dict[str, dict[str, Any]] = {
    "mifid_investment_firms": {
        "granted": True,
        "scope": "EU investment firms — FCA Overseas Persons Exclusion (OPE)",
        "notes": "EU firms can access UK professional/eligible counterparty clients via OPE without FCA authorisation",
    },
    "payment_institutions": {
        "granted": False,
        "scope": "EU payment institutions",
        "notes": "EU PIs require FCA authorisation or registration to operate in UK",
    },
    "aifmd_fund_managers": {
        "granted": True,
        "scope": "EU AIFMs — UK NPPR (National Private Placement Regime)",
        "notes": "EU AIFMs can market to UK professional investors via NPPR with FCA notification",
    },
}


def brexit_passporting_check(entity_data: dict[str, Any]) -> dict[str, Any]:
    """Determine post-Brexit licensing requirements for UK-EU cross-border services.

    Confirms that EEA passporting definitively ended on 31 December 2020 under
    the EU Withdrawal Agreement. Evaluates available equivalence decisions and
    determines what local authorisation is needed per target market.

    Args:
        entity_data: Dictionary with registered_jurisdiction, target_markets,
            license_type, has_uk_branch, has_eu_branch, and is_third_country_firm.

    Returns:
        Dictionary with keys:
            status (str): "success" or "error".
            passporting_available (bool): Always False post-Brexit for UK-EU.
            required_licenses (list[dict]): Per-market licence requirements.
            equivalence_status (dict): Applicable equivalence decisions.
            recommendations (list[str]): Strategic licensing recommendations.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        registered_jurisdiction: str = str(entity_data.get("registered_jurisdiction", "")).upper()
        target_markets: list[str] = [str(m).upper() for m in entity_data.get("target_markets", [])]
        license_type: str = str(entity_data.get("license_type", "investment_firm")).lower()
        has_uk_branch: bool = bool(entity_data.get("has_uk_branch", False))
        has_eu_branch: bool = bool(entity_data.get("has_eu_branch", False))
        is_third_country: bool = bool(entity_data.get("is_third_country_firm", False))

        required_licenses: list[dict[str, str]] = []
        recommendations: list[str] = []
        equivalence_status: dict[str, Any] = {}

        # --- Post-Brexit Passporting Confirmation ---
        # EEA passporting definitively ended 31 December 2020 (EU Withdrawal Agreement Art. 126)
        passporting_available = False  # Always False

        is_uk_authorised = registered_jurisdiction == "GB"
        is_eu_authorised = registered_jurisdiction in _EU_EEA_COUNTRIES

        # --- Determine cross-border direction ---
        uk_into_eu = is_uk_authorised and any(m in _EU_EEA_COUNTRIES for m in target_markets)
        eu_into_uk = is_eu_authorised and "GB" in target_markets

        # --- Equivalence Assessment ---
        if uk_into_eu:
            equivalence_status["direction"] = "UK firm into EU"
            equivalence_status["passporting_ended"] = "31 December 2020"
            equivalence_status["framework"] = "EU Withdrawal Agreement — Transition Period ended"

            eq_investment = _EU_UK_EQUIVALENCE.get("mifid_investment_firms", {})
            equivalence_status["mifid_equivalence"] = {
                "granted": False,
                "notes": (
                    "EU has not granted MiFIR Art. 47 equivalence to UK. "
                    "UK investment firms cannot passport into EU. "
                    "Must obtain local authorisation in each target member state."
                ),
            }
            equivalence_status["ccp_equivalence"] = _EU_UK_EQUIVALENCE.get("CCPs", {})
            equivalence_status["aifmd_nppr"] = {
                "available": license_type == "fund_manager",
                "notes": (
                    "UK AIFMs can access EU professional investors via each member state's "
                    "National Private Placement Regime (NPPR) — varies by country."
                ),
            }

        if eu_into_uk:
            equivalence_status["direction"] = "EU firm into UK"
            equivalence_status["ope_available"] = (
                license_type == "investment_firm" and not is_third_country
            )
            equivalence_status["ope_notes"] = (
                "EU investment firms may access UK professional/ECPs via Overseas Persons "
                "Exclusion (OPE) under RAO Article 72. Retail access requires FCA authorisation."
            )
            equivalence_status["nppr_available"] = license_type == "fund_manager"
            equivalence_status["nppr_notes"] = (
                "EU AIFMs can market to UK professional investors via UK NPPR with FCA notification."
            )

        # --- Per-Market Licence Requirements ---
        for market in target_markets:
            authority_map = _COMPETENT_AUTHORITIES.get(market, {})
            authority = authority_map.get(license_type, f"National regulator of {market}")

            if market in _EU_EEA_COUNTRIES and is_uk_authorised:
                # UK firm needs local EU licence
                entry = {
                    "market": market,
                    "license_type": _map_license_to_local(license_type, market),
                    "authority": authority,
                    "requirement": "Full local authorisation required — no passporting",
                    "alternatives": [],
                }

                # AIFMD NPPR alternative for fund managers
                if license_type == "fund_manager":
                    entry["alternatives"].append(
                        f"NPPR notification to {authority} — allows marketing to professional "
                        f"investors in {market} without full AIFMD authorisation"
                    )

                # Reverse solicitation for investment firms
                if license_type == "investment_firm":
                    entry["alternatives"].append(
                        f"Reverse solicitation only (client-initiated) — no marketing permitted "
                        f"in {market} without MiFID II local authorisation"
                    )

                required_licenses.append(entry)

            elif market == "GB" and is_eu_authorised:
                # EU firm needs UK FCA authorisation (with OPE/NPPR exceptions)
                if license_type == "investment_firm":
                    entry = {
                        "market": "GB",
                        "license_type": "FCA Authorisation (Part IV Permission)",
                        "authority": "FCA",
                        "requirement": (
                            "FCA authorisation required for retail access. "
                            "OPE available for wholesale/professional/ECP clients only."
                        ),
                        "alternatives": ["Overseas Persons Exclusion (OPE) for wholesale clients"],
                    }
                elif license_type == "fund_manager":
                    entry = {
                        "market": "GB",
                        "license_type": "FCA Authorisation or NPPR Notification",
                        "authority": "FCA",
                        "requirement": "NPPR notification for professional investors; FCA auth for retail",
                        "alternatives": ["UK NPPR notification (professional investors only)"],
                    }
                else:
                    entry = {
                        "market": "GB",
                        "license_type": "FCA Authorisation",
                        "authority": "FCA",
                        "requirement": "Full FCA authorisation required",
                        "alternatives": [],
                    }
                required_licenses.append(entry)

            elif market not in _EU_EEA_COUNTRIES and market != "GB":
                # Third-country market
                required_licenses.append({
                    "market": market,
                    "license_type": "Local financial services licence",
                    "authority": f"National financial regulator of {market}",
                    "requirement": "Consult local counsel — country-specific regime applies",
                    "alternatives": [],
                })

        # --- Strategic Recommendations ---
        if uk_into_eu and len(required_licenses) > 2:
            recommendations.append(
                "Consider establishing an EU legal entity (hub strategy) in a single member state "
                "(Ireland, Luxembourg, or Netherlands are common choices) to passport within the EEA, "
                "reducing the need for multiple local authorisations"
            )
            recommendations.append(
                "Ireland (CBI) and Luxembourg (CSSF) offer relatively streamlined authorisation "
                "for investment firms and fund managers with strong precedent for UK firm relocations"
            )

        if has_eu_branch and is_uk_authorised:
            recommendations.append(
                "Existing EU branch may need to be upgraded to a full subsidiary to obtain "
                "EEA passporting rights — branch authorisations do not passport across member states"
            )

        recommendations.append(
            "Maintain Temporary Permissions Regime (TPR) or Overseas Funds Regime (OFR) "
            "registrations in the UK if transitional relief is available for your firm type"
        )
        recommendations.append(
            "Review reverse solicitation documentation: EU clients may initiate contact with "
            "UK firms without local authorisation, but marketing is strictly prohibited — "
            "document all inbound enquiries (ESMA Opinion on MiFID II third-country firms, 2021)"
        )
        recommendations.append(
            "Monitor EU-UK MoU on financial services regulatory co-operation — "
            "additional equivalence decisions may be agreed bilaterally"
        )

        result = {
            "passporting_available": passporting_available,
            "passporting_ended_date": "2020-12-31",
            "passporting_legal_basis": "EU Withdrawal Agreement Art. 126; EUWA 2018",
            "registered_jurisdiction": registered_jurisdiction,
            "target_markets": target_markets,
            "license_type": license_type,
            "has_uk_branch": has_uk_branch,
            "has_eu_branch": has_eu_branch,
            "required_licenses": required_licenses,
            "equivalence_status": equivalence_status,
            "recommendations": recommendations,
            "key_resources": [
                "FCA Temporary Permissions Regime: fca.org.uk/brexit",
                "EBA Opinion on equivalence: eba.europa.eu",
                "ESMA Q&A on MiFID II third-country firms (2021)",
                "EU Withdrawal Agreement (OJ L 29, 31.1.2020)",
            ],
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"brexit_passporting_check failed: {e}")
        _log_lesson(f"brexit_passporting_check: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _map_license_to_local(license_type: str, market: str) -> str:
    """Map a generic licence type to the local EU regulatory instrument name.

    Args:
        license_type: Generic licence type string.
        market: ISO 3166-1 alpha-2 country code.

    Returns:
        Local regulatory licence name string.
    """
    mapping = {
        "investment_firm": "MiFID II Investment Firm Authorisation",
        "credit_institution": "CRD V Credit Institution Licence",
        "payment_institution": "PSD2 Payment Institution Authorisation",
        "e_money": "EMD2 E-Money Institution Authorisation",
        "fund_manager": "AIFMD / UCITS Management Company Authorisation",
        "insurance": "Solvency II Insurance Undertaking Authorisation",
    }
    return mapping.get(license_type, f"Local financial services licence ({market})")


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
