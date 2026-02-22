"""
Executive Summary: Nation fiat-to-digital treasury onboarding — converts sovereign currency to digital assets with regulatory surcharges and settlement estimates.
Inputs: conversion (dict: source_currency str, target_digital_asset str, amount float,
        exchange_rate float, regulatory_jurisdiction str)
Outputs: converted_amount (float), total_fees (float), settlement_hours (int),
         regulatory_requirements (list), conversion_rate_used (float)
MCP Tool Name: sovereign_fiat_bridge
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

# Regulatory surcharge table: jurisdiction → surcharge decimal
JURISDICTION_SURCHARGES: dict[str, float] = {
    "US":  0.001,   # 0.1% FinCEN compliance overhead
    "EU":  0.0015,  # 0.15% MiCA regulatory cost
    "UK":  0.001,   # 0.1% FCA
    "SG":  0.0005,  # 0.05% MAS — favourable
    "AE":  0.0005,  # 0.05% ADGM / VARA — favourable
    "CH":  0.001,   # 0.1% FINMA
    "JP":  0.002,   # 0.2% FSA — elevated
    "KR":  0.0025,  # 0.25% FSC — elevated
    "CN":  0.05,    # 5% — extreme regulatory friction
    "DEFAULT": 0.002,  # 0.2% catch-all for unlisted jurisdictions
}

# Settlement time (hours) by jurisdiction
SETTLEMENT_HOURS: dict[str, int] = {
    "US":  24,
    "EU":  12,
    "UK":  12,
    "SG":  6,
    "AE":  6,
    "CH":  12,
    "JP":  24,
    "KR":  24,
    "CN":  72,
    "DEFAULT": 48,
}

# Regulatory requirements by jurisdiction
REGULATORY_REQUIREMENTS: dict[str, list[str]] = {
    "US":  ["FinCEN MSB registration", "BSA/AML program", "SAR filing capability"],
    "EU":  ["MiCA license or exemption", "GDPR data residency", "VASP registration"],
    "UK":  ["FCA cryptoasset registration", "AML/CTF compliance", "Travel Rule adherence"],
    "SG":  ["MAS PSA license", "Travel Rule (FATF)", "Customer due diligence"],
    "AE":  ["ADGM or VARA license", "AML program", "Sanctions screening"],
    "CH":  ["FINMA VQF or SRO membership", "AML Act compliance"],
    "JP":  ["FSA CAESS registration", "Cold storage requirements", "Segregated client funds"],
    "KR":  ["FSC VASP registration", "KYC real-name accounts", "Banking partner required"],
    "CN":  ["PBOC approval (currently suspended)", "Cross-border restrictions apply"],
    "DEFAULT": ["FATF Travel Rule", "KYC/AML program", "Sanctions screening"],
}

# Base protocol fee (flat decimal applied to conversion amount)
BASE_PROTOCOL_FEE: float = 0.002  # 0.2%

TOOL_META = {
    "name": "sovereign_fiat_bridge",
    "description": (
        "Converts sovereign fiat currency to a target digital asset for treasury "
        "onboarding. Applies jurisdiction-specific regulatory surcharges on top of a "
        "base protocol fee. Estimates settlement time and enumerates regulatory "
        "requirements for the given jurisdiction."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "conversion": {
                "type": "object",
                "properties": {
                    "source_currency":         {"type": "string"},
                    "target_digital_asset":    {"type": "string"},
                    "amount":                  {"type": "number"},
                    "exchange_rate":           {"type": "number"},
                    "regulatory_jurisdiction": {"type": "string"},
                },
                "required": [
                    "source_currency", "target_digital_asset",
                    "amount", "exchange_rate", "regulatory_jurisdiction"
                ],
            }
        },
        "required": ["conversion"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "converted_amount":        {"type": "number"},
            "total_fees":              {"type": "number"},
            "settlement_hours":        {"type": "integer"},
            "regulatory_requirements": {"type": "array"},
            "conversion_rate_used":    {"type": "number"},
            "fee_breakdown":           {"type": "object"},
            "status":                  {"type": "string"},
            "timestamp":               {"type": "string"},
        },
        "required": [
            "converted_amount", "total_fees", "settlement_hours",
            "regulatory_requirements", "conversion_rate_used", "status", "timestamp"
        ],
    },
}


def sovereign_fiat_bridge(conversion: dict[str, Any]) -> dict[str, Any]:
    """Bridge sovereign fiat currency to a digital asset for treasury onboarding.

    Args:
        conversion: Conversion parameters with keys:
            - source_currency (str): ISO 4217 currency code (e.g. "USD", "EUR").
            - target_digital_asset (str): Digital asset ticker (e.g. "USDC", "TON").
            - amount (float): Amount of source currency to convert.
            - exchange_rate (float): Units of digital asset per one unit of fiat.
            - regulatory_jurisdiction (str): ISO country code of governing jurisdiction.

    Returns:
        dict with keys:
            - status (str): "success" or "error".
            - converted_amount (float): Digital asset units received after fees.
            - total_fees (float): Total fees in source currency units.
            - settlement_hours (int): Estimated settlement window.
            - regulatory_requirements (list[str]): Applicable regulatory obligations.
            - conversion_rate_used (float): The exchange_rate applied.
            - fee_breakdown (dict): Itemised fee components.
            - timestamp (str): ISO 8601 UTC execution timestamp.
    """
    try:
        now_utc: datetime = datetime.now(timezone.utc)

        source_currency: str = str(conversion.get("source_currency", "")).upper()
        target_asset: str = str(conversion.get("target_digital_asset", "")).upper()
        amount: float = float(conversion.get("amount", 0.0))
        exchange_rate: float = float(conversion.get("exchange_rate", 1.0))
        jurisdiction: str = str(conversion.get("regulatory_jurisdiction", "")).upper()

        if amount <= 0:
            raise ValueError("amount must be positive.")
        if exchange_rate <= 0:
            raise ValueError("exchange_rate must be positive.")

        # Fee calculation
        base_fee: float = round(amount * BASE_PROTOCOL_FEE, 6)
        surcharge_rate: float = JURISDICTION_SURCHARGES.get(
            jurisdiction, JURISDICTION_SURCHARGES["DEFAULT"]
        )
        regulatory_surcharge: float = round(amount * surcharge_rate, 6)
        total_fees: float = round(base_fee + regulatory_surcharge, 6)

        # Net amount after fees, then convert to digital asset
        net_fiat: float = amount - total_fees
        converted_amount: float = round(net_fiat * exchange_rate, 8)

        settlement_hours: int = SETTLEMENT_HOURS.get(
            jurisdiction, SETTLEMENT_HOURS["DEFAULT"]
        )
        regulatory_requirements: list[str] = REGULATORY_REQUIREMENTS.get(
            jurisdiction, REGULATORY_REQUIREMENTS["DEFAULT"]
        )

        fee_breakdown: dict[str, Any] = {
            "gross_amount":          amount,
            "base_protocol_fee":     base_fee,
            "base_protocol_rate":    BASE_PROTOCOL_FEE,
            "regulatory_surcharge":  regulatory_surcharge,
            "surcharge_rate":        surcharge_rate,
            "total_fees":            total_fees,
            "net_fiat_after_fees":   round(net_fiat, 6),
        }

        return {
            "status":                  "success",
            "converted_amount":        converted_amount,
            "total_fees":              total_fees,
            "settlement_hours":        settlement_hours,
            "regulatory_requirements": regulatory_requirements,
            "conversion_rate_used":    exchange_rate,
            "fee_breakdown":           fee_breakdown,
            "timestamp":               now_utc.isoformat(),
        }

    except Exception as e:
        logger.error(f"sovereign_fiat_bridge failed: {e}")
        _log_lesson(f"sovereign_fiat_bridge: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Append a failure lesson to the shared lessons log.

    Args:
        message: Human-readable description of the failure.
    """
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
