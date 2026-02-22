"""
Executive Summary: Tracks a country's IMF Special Drawing Rights position, converting to USD, measuring SDR usage against allocations, and assessing quota adequacy.
Inputs: country_data (dict: country, quota_pct, sdr_holdings, sdr_allocations, gdp_usd), sdr_usd_rate (float)
Outputs: holdings_usd (float), allocation_usd (float), net_position (float), usage_pct (float), quota_adequacy (str)
MCP Tool Name: imf_sdr_allocation_tracker
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "imf_sdr_allocation_tracker",
    "description": "Tracks IMF Special Drawing Rights (SDR) holdings vs allocations for a country, converts to USD, and assesses quota adequacy.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "country_data": {
                "type": "object",
                "description": "Country SDR and economic data",
                "properties": {
                    "country": {"type": "string", "description": "Country name or ISO code"},
                    "quota_pct": {"type": "number", "description": "Country's share of IMF total quota (%)"},
                    "sdr_holdings": {"type": "number", "description": "Current SDR holdings in SDR units"},
                    "sdr_allocations": {"type": "number", "description": "Total SDR allocated by IMF to this country"},
                    "gdp_usd": {"type": "number", "description": "Country GDP in USD (optional, for context)"}
                },
                "required": ["country", "quota_pct", "sdr_holdings", "sdr_allocations"]
            },
            "sdr_usd_rate": {
                "type": "number",
                "description": "Current SDR to USD exchange rate (e.g. 1.33)"
            },
            "total_imf_sdrs": {
                "type": "number",
                "description": "Total IMF SDR allocation pool in SDR units (default: 660 billion)"
            }
        },
        "required": ["country_data", "sdr_usd_rate"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "holdings_usd": {"type": "number"},
                    "allocation_usd": {"type": "number"},
                    "net_position": {"type": "number"},
                    "usage_pct": {"type": "float"},
                    "quota_adequacy": {"type": "string"}
                }
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "data", "timestamp"]
    }
}

# Total IMF SDR pool post-2021 allocation (approx. 660 billion SDRs)
DEFAULT_TOTAL_IMF_SDRS = 660_000_000_000.0

# SDR interest rate charge threshold: countries pay if they use SDRs beyond allocation
# Approximation of IMF SDR interest rate as of 2025
SDR_INTEREST_RATE_APPROX = 0.0388  # ~3.88% per year (IMF SDR rate 2025)


def imf_sdr_allocation_tracker(
    country_data: dict[str, Any],
    sdr_usd_rate: float,
    total_imf_sdrs: float | None = None,
    **kwargs: Any
) -> dict[str, Any]:
    """Track a country's IMF SDR position and assess quota adequacy.

    SDR mechanics:
      - Countries receive SDR allocations proportional to their IMF quota.
      - If holdings < allocations, the country has USED SDRs (drew down reserves).
        It owes the SDR interest rate on the shortfall.
      - If holdings > allocations, the country is a NET LENDER and earns interest.
      - Net position = holdings - allocations (negative = used/borrowed).

    Args:
        country_data: Dictionary containing:
            - country (str): Country name or ISO code.
            - quota_pct (float): Country's share of IMF total quota as %.
            - sdr_holdings (float): Current SDR holdings in SDR units.
            - sdr_allocations (float): Total SDR allocated by IMF.
            - gdp_usd (float, optional): GDP in USD for context ratios.
        sdr_usd_rate: Current market exchange rate of 1 SDR in USD.
        total_imf_sdrs: Total IMF SDR pool (defaults to 660 billion SDR).
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Standard Snowdrop response envelope with keys:
            - status (str): 'success' or 'error'.
            - data (dict): SDR analysis including holdings_usd, allocation_usd,
              net_position (SDR units), net_position_usd, usage_pct,
              quota_adequacy, interest_cost_usd (if net borrower),
              quota_consistency_check, and gdp_ratios (if gdp provided).
            - timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        country = str(country_data.get("country", "UNKNOWN")).strip()
        quota_pct = float(country_data.get("quota_pct", 0.0))
        sdr_holdings = float(country_data.get("sdr_holdings", 0.0))
        sdr_allocations = float(country_data.get("sdr_allocations", 0.0))
        gdp_usd = country_data.get("gdp_usd")
        if gdp_usd is not None:
            gdp_usd = float(gdp_usd)

        sdr_usd_rate = float(sdr_usd_rate)
        pool_size = float(total_imf_sdrs) if total_imf_sdrs else DEFAULT_TOTAL_IMF_SDRS

        if sdr_usd_rate <= 0:
            raise ValueError("sdr_usd_rate must be positive")
        if quota_pct < 0 or quota_pct > 100:
            raise ValueError("quota_pct must be between 0 and 100")

        # Core calculations
        holdings_usd: float = round(sdr_holdings * sdr_usd_rate, 2)
        allocation_usd: float = round(sdr_allocations * sdr_usd_rate, 2)
        net_position: float = round(sdr_holdings - sdr_allocations, 4)  # SDR units
        net_position_usd: float = round(net_position * sdr_usd_rate, 2)

        # Usage calculation: SDRs used = allocations - holdings (if positive)
        sdrs_used = max(0.0, sdr_allocations - sdr_holdings)
        usage_pct: float = round(sdrs_used / sdr_allocations * 100, 4) if sdr_allocations > 0 else 0.0

        # Position type
        if net_position > 0:
            position_type = "NET_LENDER"
            interest_earned_usd = round(net_position * sdr_usd_rate * SDR_INTEREST_RATE_APPROX, 2)
            interest_cost_usd = 0.0
        elif net_position < 0:
            position_type = "NET_BORROWER"
            interest_earned_usd = 0.0
            interest_cost_usd = round(abs(net_position) * sdr_usd_rate * SDR_INTEREST_RATE_APPROX, 2)
        else:
            position_type = "FULLY_RETAINED"
            interest_earned_usd = 0.0
            interest_cost_usd = 0.0

        # Quota consistency check: expected allocation based on quota_pct
        expected_allocation = round(quota_pct / 100.0 * pool_size, 4)
        allocation_vs_quota_delta = round(sdr_allocations - expected_allocation, 4)
        quota_consistent = abs(allocation_vs_quota_delta) < expected_allocation * 0.05  # within 5%

        # Quota adequacy assessment
        if usage_pct == 0 and net_position >= 0:
            quota_adequacy = "SURPLUS — Country holds more SDRs than allocated; acts as net liquidity provider to IMF system"
        elif usage_pct < 25:
            quota_adequacy = "ADEQUATE — Minimal SDR usage; strong external liquidity position"
        elif usage_pct < 50:
            quota_adequacy = "MODERATE_USE — Country has drawn on ~half its SDR allocation; monitor external account"
        elif usage_pct < 80:
            quota_adequacy = "HEAVY_USE — Country has used majority of SDR allocation; potential BOP pressure"
        elif usage_pct < 100:
            quota_adequacy = "NEAR_LIMIT — SDR allocation nearly exhausted; IMF program or quota increase may be needed"
        else:
            quota_adequacy = "EXCEEDED — Holdings below zero or allocation overdrawn; country may need emergency IMF facility"

        # GDP ratios (if provided)
        gdp_ratios: dict[str, Any] = {}
        if gdp_usd and gdp_usd > 0:
            gdp_ratios = {
                "holdings_pct_gdp": round(holdings_usd / gdp_usd * 100, 4),
                "allocation_pct_gdp": round(allocation_usd / gdp_usd * 100, 4),
                "net_position_pct_gdp": round(net_position_usd / gdp_usd * 100, 4),
                "gdp_usd": gdp_usd,
            }

        result: dict[str, Any] = {
            "country": country,
            "sdr_usd_rate": sdr_usd_rate,
            "holdings_sdr": sdr_holdings,
            "holdings_usd": holdings_usd,
            "allocation_sdr": sdr_allocations,
            "allocation_usd": allocation_usd,
            "net_position": net_position,
            "net_position_usd": net_position_usd,
            "sdrs_used": round(sdrs_used, 4),
            "usage_pct": usage_pct,
            "position_type": position_type,
            "quota_adequacy": quota_adequacy,
            "quota_pct": quota_pct,
            "expected_allocation_sdr": expected_allocation,
            "allocation_vs_quota_delta": allocation_vs_quota_delta,
            "quota_consistent": quota_consistent,
            "interest_cost_usd_annual": interest_cost_usd,
            "interest_earned_usd_annual": interest_earned_usd,
            "sdr_interest_rate_pct": round(SDR_INTEREST_RATE_APPROX * 100, 4),
            "gdp_ratios": gdp_ratios,
            "total_imf_pool_sdr": pool_size,
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"imf_sdr_allocation_tracker failed: {e}")
        _log_lesson(f"imf_sdr_allocation_tracker: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append a lesson/error entry to the shared lessons log.

    Args:
        message: Human-readable error or lesson description to append.
    """
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except Exception as log_err:
        logger.warning(f"_log_lesson write failed: {log_err}")
