"""
Executive Summary: Australian ASIC financial services licensing checker — determines AFSL requirements, wholesale/retail client classifications, foreign provider relief, and required authorisations per Corporations Act 2001.
Inputs: entity_data (dict: service_type, client_type, product_types, is_foreign_provider)
Outputs: afsl_required (bool), exemptions_available (list), required_authorizations (list), foreign_provider_relief (bool)
MCP Tool Name: australia_asics_checker
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "australia_asics_checker",
    "description": (
        "Determines Australian Financial Services Licence (AFSL) requirements under the "
        "Corporations Act 2001 (Cth) Part 7.6. Evaluates service type, client classification "
        "(retail vs wholesale), product categories, and foreign provider relief under "
        "ASIC Class Orders and legislative instruments."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "entity_data": {
                "type": "object",
                "properties": {
                    "service_type": {
                        "type": "string",
                        "description": "financial_product_advice / dealing / market_making / custody / payment / managed_investments",
                    },
                    "client_type": {
                        "type": "string",
                        "description": "retail / wholesale / both",
                        "enum": ["retail", "wholesale", "both"],
                    },
                    "product_types": {
                        "type": "array",
                        "description": "List of financial products: securities / derivatives / managed_investment_schemes / deposit_products / insurance / superannuation / crypto_assets",
                        "items": {"type": "string"},
                    },
                    "is_foreign_provider": {
                        "type": "boolean",
                        "description": "True if the entity is incorporated / authorised outside Australia",
                    },
                    "home_jurisdiction": {
                        "type": "string",
                        "description": "ISO 3166-1 alpha-2 country code of the entity's home regulator jurisdiction",
                    },
                    "provides_general_advice_only": {
                        "type": "boolean",
                        "description": "True if entity only provides general (not personal) financial product advice",
                    },
                    "aum_aud": {
                        "type": "number",
                        "description": "Assets under management in AUD (for wholesale threshold checks)",
                    },
                    "entity_net_assets_aud": {
                        "type": "number",
                        "description": "Net assets in AUD (for wholesale entity threshold A$10M)",
                    },
                },
                "required": ["service_type", "client_type", "product_types", "is_foreign_provider"],
            }
        },
        "required": ["entity_data"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "afsl_required": {"type": "boolean"},
            "exemptions_available": {"type": "array", "items": {"type": "string"}},
            "required_authorizations": {"type": "array", "items": {"type": "string"}},
            "foreign_provider_relief": {"type": "boolean"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": [
            "afsl_required",
            "exemptions_available",
            "required_authorizations",
            "foreign_provider_relief",
            "status",
            "timestamp",
        ],
    },
}

# Wholesale client thresholds (Corporations Act s. 761G)
_WHOLESALE_NET_ASSETS_AUD = 10_000_000   # A$10M net assets
_WHOLESALE_GROSS_INCOME_AUD = 250_000    # A$250K gross income (12 months)

# ASIC-designated equivalent foreign jurisdictions for Class Order relief
# ASIC Corporations (Foreign Financial Services Providers) Instrument 2020/198
_EQUIVALENT_JURISDICTIONS: set[str] = {
    "US",  # SEC / CFTC regulated entities
    "GB",  # FCA regulated entities
    "CA",  # OSC / IIROC regulated entities
    "DE",  # BaFin regulated entities
    "FR",  # AMF regulated entities
    "SG",  # MAS regulated entities
    "HK",  # SFC regulated entities
    "JP",  # FSA Japan regulated entities
    "NZ",  # FMA NZ regulated entities
    "LU",  # CSSF regulated entities
    "IE",  # CBI regulated entities
    "NL",  # AFM/DNB regulated entities
    "SE",  # Finansinspektionen regulated entities
    "CH",  # FINMA regulated entities
    "DK",  # Finanstilsynet regulated entities
}

# Products that require specific AFSL authorisations
_PRODUCT_AUTHORISATIONS: dict[str, str] = {
    "securities": "Authorisation to deal in / advise on securities (s. 764A(1)(a) Corporations Act)",
    "derivatives": "Authorisation to deal in / advise on derivatives (s. 764A(1)(b))",
    "managed_investment_schemes": (
        "Authorisation to operate / advise on managed investment schemes (s. 764A(1)(b), Ch. 5C)"
    ),
    "deposit_products": "Authorisation to deal in / advise on deposit accounts (s. 764A(1)(e))",
    "insurance": "Authorisation to deal in / advise on insurance products (s. 764A(1)(d))",
    "superannuation": "Authorisation to advise on / deal in superannuation interests (s. 764A(1)(f))",
    "crypto_assets": (
        "ASIC INFO 225: crypto-assets that are financial products require AFSL. "
        "Currency exchange products may be exempt. ASIC legal opinion recommended."
    ),
    "margin_lending": "Authorisation to provide margin lending facilities (s. 764A(1)(ba))",
    "foreign_exchange": "Authorisation to deal in foreign exchange contracts (s. 764A(1)(b))",
}


def australia_asics_checker(entity_data: dict[str, Any]) -> dict[str, Any]:
    """Determine AFSL requirements for providing financial services in Australia.

    Evaluates service type, client classification, and product types to
    determine AFSL obligation. For foreign providers, checks ASIC relief
    instruments and equivalent jurisdiction status.

    Args:
        entity_data: Dictionary with service_type, client_type, product_types,
            is_foreign_provider, home_jurisdiction, provides_general_advice_only,
            aum_aud, and entity_net_assets_aud.

    Returns:
        Dictionary with keys:
            status (str): "success" or "error".
            afsl_required (bool): Whether an AFSL is required.
            exemptions_available (list[str]): Applicable exemptions or relief.
            required_authorizations (list[str]): Specific AFSL authorisations needed.
            foreign_provider_relief (bool): Whether foreign provider relief applies.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        service_type: str = str(entity_data.get("service_type", "")).lower().replace(" ", "_")
        client_type: str = str(entity_data.get("client_type", "retail")).lower()
        product_types: list[str] = [str(p).lower() for p in entity_data.get("product_types", [])]
        is_foreign: bool = bool(entity_data.get("is_foreign_provider", False))
        home_jurisdiction: str = str(entity_data.get("home_jurisdiction", "")).upper()
        general_advice_only: bool = bool(entity_data.get("provides_general_advice_only", False))
        aum_aud: float = float(entity_data.get("aum_aud", 0))
        entity_net_assets: float = float(entity_data.get("entity_net_assets_aud", 0))

        exemptions_available: list[str] = []
        required_authorizations: list[str] = []
        afsl_required = True
        foreign_provider_relief = False

        # =====================================================================
        # WHOLESALE-ONLY EXEMPTIONS
        # Corporations Act s. 911A(2)(d): no AFSL required if only wholesale clients
        # =====================================================================
        if client_type == "wholesale":
            # Wholesale client definition: s. 761G — net assets >= A$10M or gross income >= A$250K
            exemptions_available.append(
                "Wholesale-only exemption: Corporations Act s. 911A(2)(d) — no AFSL required "
                "when providing financial services exclusively to wholesale clients. "
                "Wholesale client thresholds: net assets >= A$10M or gross income >= A$250K p.a. "
                "(s. 761G). Accountant's certificate must be obtained within 2 years."
            )
            # Some product types still require AFSL even for wholesale
            wholesale_always_afsl = [p for p in product_types if p in {"managed_investment_schemes", "superannuation"}]
            if wholesale_always_afsl:
                exemptions_available.append(
                    f"NOTE: Wholesale exemption does not apply to: {', '.join(wholesale_always_afsl)}. "
                    "Operating a managed investment scheme requires AFSL regardless of client type "
                    "(Corporations Act s. 601FA — responsible entity must hold AFSL)."
                )
                afsl_required = True
            else:
                afsl_required = False

        # =====================================================================
        # FOREIGN PROVIDER RELIEF
        # ASIC Corporations (Foreign Financial Services Providers) Instrument 2020/198
        # Replaces old Class Orders CO 03/1099 and CO 03/1100
        # Transitional relief extended; check current ASIC website for expiry date
        # =====================================================================
        if is_foreign and home_jurisdiction in _EQUIVALENT_JURISDICTIONS:
            foreign_provider_relief = True
            exemptions_available.append(
                f"Foreign Financial Service Provider (FFSP) Relief available: "
                f"Home jurisdiction '{home_jurisdiction}' is an ASIC-designated equivalent "
                "regulator jurisdiction under ASIC Corporations (Foreign Financial Services "
                "Providers) Instrument 2020/198. AFSL not required for wholesale client services "
                "provided on 'sufficient equivalence' basis. Must lodge notification with ASIC."
            )
            exemptions_available.append(
                "FFSP Relief conditions: (1) must be licensed by equivalent overseas regulator, "
                "(2) services only to wholesale clients, (3) annual notification lodged with ASIC, "
                "(4) relief does not extend to retail clients — retail requires AFSL."
            )
            if client_type in {"retail", "both"}:
                exemptions_available.append(
                    "WARNING: FFSP relief covers WHOLESALE clients only. "
                    "Retail client services require a full AFSL under s. 911A(1). "
                    "Consider appointing an Australian AFSL holder as authorised representative "
                    "for retail distribution."
                )
                afsl_required = True
            else:
                afsl_required = False  # Wholesale foreign provider gets relief

        elif is_foreign and home_jurisdiction not in _EQUIVALENT_JURISDICTIONS:
            foreign_provider_relief = False
            exemptions_available.append(
                f"Foreign provider from non-equivalent jurisdiction '{home_jurisdiction}': "
                "No ASIC foreign relief available. Full AFSL required. Consider establishing "
                "an Australian subsidiary or appointing an AFSL-holder as representative."
            )

        # =====================================================================
        # GENERAL ADVICE ONLY (NO PERSONAL ADVICE)
        # =====================================================================
        if general_advice_only and client_type == "wholesale":
            exemptions_available.append(
                "General advice to wholesale clients: limited AFSL authorisations sufficient. "
                "No personal advice obligation (best interest duty, s. 961B) applies. "
                "Scaled AFSL authorisation for 'general advice on [product types]' only."
            )

        # =====================================================================
        # REQUIRED AUTHORISATIONS
        # =====================================================================
        # Build required authorisation list based on products
        for product in product_types:
            auth = _PRODUCT_AUTHORISATIONS.get(product)
            if auth:
                required_authorizations.append(auth)
            else:
                required_authorizations.append(
                    f"Review required: '{product}' — determine if it is a financial product "
                    "under Corporations Act s. 764A or Regulations r. 7.1.04"
                )

        # Service-specific authorisations
        if service_type == "market_making":
            required_authorizations.append(
                "Market Licence required if operating a financial market (Corporations Act s. 791A). "
                "AFSL with market-making authorisation also required."
            )
        elif service_type == "custody":
            required_authorizations.append(
                "Custodial or depository services authorisation (Corporations Act s. 766E). "
                "Client assets must be held under specific custody arrangements."
            )
        elif service_type == "managed_investments":
            required_authorizations.append(
                "Responsible entity (RE) licence: must hold AFSL authorising operation of a "
                "registered managed investment scheme (Corporations Act s. 601FA, Ch. 5C)."
            )

        # =====================================================================
        # CRYPTO-SPECIFIC NOTE
        # =====================================================================
        if "crypto_assets" in product_types:
            required_authorizations.append(
                "ASIC INFO 225 (2022): crypto-assets that are financial products (e.g. exchange-traded "
                "tokens that are derivatives, managed investment scheme interests) require AFSL. "
                "Pure cryptocurrency exchange (AUD/BTC) may be AUSTRAC-registered only (AML/CTF Act). "
                "Legal opinion recommended for each token type."
            )

        # =====================================================================
        # AUTHORISED REPRESENTATIVE OPTION
        # =====================================================================
        exemptions_available.append(
            "Authorised Representative (AR) alternative: instead of holding an AFSL, "
            "an entity can become an Authorised Representative of an existing AFSL holder "
            "(Corporations Act s. 916A). The AFSL holder bears licence obligations. "
            "Common for foreign firms and fintech startups."
        )

        result = {
            "afsl_required": afsl_required,
            "service_type": service_type,
            "client_type": client_type,
            "product_types": product_types,
            "is_foreign_provider": is_foreign,
            "home_jurisdiction": home_jurisdiction,
            "foreign_provider_relief": foreign_provider_relief,
            "equivalent_jurisdiction": home_jurisdiction in _EQUIVALENT_JURISDICTIONS if is_foreign else None,
            "exemptions_available": exemptions_available,
            "required_authorizations": required_authorizations,
            "wholesale_thresholds": {
                "net_assets_aud": _WHOLESALE_NET_ASSETS_AUD,
                "gross_income_aud_pa": _WHOLESALE_GROSS_INCOME_AUD,
            },
            "key_legislation": [
                "Corporations Act 2001 (Cth) Part 7.6 — Licensing of financial services",
                "Corporations Act s. 911A — Obligation to hold AFSL",
                "Corporations Act s. 761G — Wholesale client definition",
                "ASIC Corporations (Foreign Financial Services Providers) Instrument 2020/198",
                "Corporations Act s. 916A — Authorised representatives",
                "ASIC INFO 225 — Crypto-assets and financial products",
            ],
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"australia_asics_checker failed: {e}")
        _log_lesson(f"australia_asics_checker: {e}")
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
