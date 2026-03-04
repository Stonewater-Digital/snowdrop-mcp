"""
Executive Summary: International LP withholding — applies treaty or default withholding rates and computes net distribution.
Inputs: lp_data (dict: country str, entity_type str, treaty_country bool, distribution_amount float),
        withholding_rates (dict: default_rate float, treaty_rates dict[country→rate])
Outputs: withholding_amount (float), effective_rate (float), treaty_applied (bool), net_distribution (float)
MCP Tool Name: global_tax_withholding_skill
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

# Entity types that are always exempt from withholding
TAX_EXEMPT_ENTITY_TYPES: set[str] = {"pension_fund", "sovereign_wealth_fund", "tax_exempt_org", "charity"}

TOOL_META = {
    "name": "global_tax_withholding_skill",
    "description": (
        "Calculates the withholding tax on a distribution to an international LP. "
        "Applies any available tax treaty rate in preference to the default rate. "
        "Grants full exemption (0%) to qualifying entities such as pension funds and "
        "sovereign wealth funds. Returns the withholding amount, effective rate, and "
        "net distribution after withholding."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "lp_data": {
                "type": "object",
                "properties": {
                    "country":             {"type": "string"},
                    "entity_type":         {"type": "string"},
                    "treaty_country":      {"type": "boolean"},
                    "distribution_amount": {"type": "number"},
                },
                "required": ["country", "entity_type", "treaty_country", "distribution_amount"],
            },
            "withholding_rates": {
                "type": "object",
                "properties": {
                    "default_rate":  {"type": "number", "description": "Rate as decimal, e.g. 0.30 for 30%."},
                    "treaty_rates":  {
                        "type": "object",
                        "additionalProperties": {"type": "number"},
                        "description": "Map of country code → withholding rate decimal.",
                    },
                },
                "required": ["default_rate"],
            },
        },
        "required": ["lp_data", "withholding_rates"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "withholding_amount": {"type": "number"},
            "effective_rate":     {"type": "number"},
            "treaty_applied":     {"type": "boolean"},
            "net_distribution":   {"type": "number"},
            "exemption_applied":  {"type": "boolean"},
            "exemption_reason":   {"type": ["string", "null"]},
            "status":             {"type": "string"},
            "timestamp":          {"type": "string"},
        },
        "required": [
            "withholding_amount", "effective_rate", "treaty_applied",
            "net_distribution", "exemption_applied", "status", "timestamp"
        ],
    },
}


def global_tax_withholding_skill(
    lp_data: dict[str, Any],
    withholding_rates: dict[str, Any],
) -> dict[str, Any]:
    """Calculate international LP withholding tax and net distribution.

    Rate precedence (highest to lowest priority):
        1. Exempt entity — 0% (pension funds, sovereign wealth funds, etc.)
        2. Treaty rate — if LP country has a tax treaty entry in withholding_rates.
        3. Default withholding rate.

    Args:
        lp_data: Limited partner profile with keys:
            - country (str): ISO country code of the LP (e.g. "CA", "DE").
            - entity_type (str): LP classification, e.g. "pension_fund", "individual".
            - treaty_country (bool): Whether the LP's country has a tax treaty.
            - distribution_amount (float): Gross distribution amount in USD.
        withholding_rates: Rate table with keys:
            - default_rate (float): Fallback rate as a decimal (e.g. 0.30).
            - treaty_rates (dict, optional): Map of country code to rate decimal.

    Returns:
        dict with keys:
            - status (str): "success" or "error".
            - withholding_amount (float): USD amount withheld.
            - effective_rate (float): Applied rate as a decimal.
            - treaty_applied (bool): True if a treaty rate was used.
            - net_distribution (float): Amount remitted after withholding.
            - exemption_applied (bool): True if entity-type exemption granted.
            - exemption_reason (str | None): Human-readable explanation for exemption.
            - timestamp (str): ISO 8601 UTC execution timestamp.
    """
    try:
        now_utc: datetime = datetime.now(timezone.utc)

        country: str = lp_data.get("country", "").upper()
        entity_type: str = lp_data.get("entity_type", "").lower()
        treaty_country: bool = bool(lp_data.get("treaty_country", False))
        distribution_amount: float = float(lp_data.get("distribution_amount", 0.0))

        default_rate: float = float(withholding_rates.get("default_rate", 0.30))
        treaty_rates: dict[str, float] = {
            k.upper(): float(v)
            for k, v in withholding_rates.get("treaty_rates", {}).items()
        }

        effective_rate: float = default_rate
        treaty_applied: bool = False
        exemption_applied: bool = False
        exemption_reason: str | None = None

        # Priority 1: Exempt entity types
        if entity_type in TAX_EXEMPT_ENTITY_TYPES:
            effective_rate = 0.0
            exemption_applied = True
            exemption_reason = (
                f"Entity type '{entity_type}' qualifies for 0% withholding under "
                "tax-exempt entity provisions."
            )

        # Priority 2: Treaty rate
        elif treaty_country and country in treaty_rates:
            effective_rate = treaty_rates[country]
            treaty_applied = True

        # Priority 3: Default rate (already set)

        withholding_amount: float = round(distribution_amount * effective_rate, 2)
        net_distribution: float = round(distribution_amount - withholding_amount, 2)

        return {
            "status":             "success",
            "withholding_amount": withholding_amount,
            "effective_rate":     effective_rate,
            "treaty_applied":     treaty_applied,
            "net_distribution":   net_distribution,
            "exemption_applied":  exemption_applied,
            "exemption_reason":   exemption_reason,
            "timestamp":          now_utc.isoformat(),
        }

    except Exception as e:
        logger.error(f"global_tax_withholding_skill failed: {e}")
        _log_lesson(f"global_tax_withholding_skill: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Append a failure lesson to the shared lessons log.

    Args:
        message: Human-readable description of the failure.
    """
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
