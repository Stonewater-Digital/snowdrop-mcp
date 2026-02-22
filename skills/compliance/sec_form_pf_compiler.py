"""
Executive Summary: US SEC Form PF compiler for private fund advisers — determines Large Adviser status, compiles systemic risk data for Section 1 and Section 2, and flags systemic risk indicators.
Inputs: fund_data (dict: fund_name, aum, nav, strategy, leverage_ratio, investor_count, redemption_terms, top_positions (list))
Outputs: form_pf_json (dict), filing_frequency (str), large_adviser (bool), systemic_risk_flags (list)
MCP Tool Name: sec_form_pf_compiler
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "sec_form_pf_compiler",
    "description": (
        "Compiles SEC Form PF data for private fund advisers under Dodd-Frank Act Section 404 "
        "and SEC Rule 204(b)-1. Determines Large Adviser classification, filing frequency, "
        "and generates the structured Form PF JSON payload for PFRD submission."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "fund_data": {
                "type": "object",
                "properties": {
                    "fund_name": {"type": "string"},
                    "aum": {"type": "number", "description": "Regulatory assets under management in USD"},
                    "nav": {"type": "number", "description": "Net asset value in USD"},
                    "strategy": {
                        "type": "string",
                        "description": "hedge_fund / liquidity_fund / private_equity / real_estate / other",
                    },
                    "leverage_ratio": {
                        "type": "number",
                        "description": "Gross leverage: total notional exposure / NAV",
                    },
                    "investor_count": {"type": "integer"},
                    "redemption_terms": {
                        "type": "string",
                        "description": "E.g. monthly_30_day_notice / quarterly / annual / locked_up / daily",
                    },
                    "top_positions": {
                        "type": "array",
                        "description": "List of top positions with asset_class and notional_usd",
                        "items": {
                            "type": "object",
                            "properties": {
                                "asset_class": {"type": "string"},
                                "notional_usd": {"type": "number"},
                                "pct_of_nav": {"type": "number"},
                            },
                        },
                    },
                    "liquidity_stress_tested": {"type": "boolean"},
                    "prime_broker": {"type": "string"},
                    "domicile": {"type": "string"},
                },
                "required": ["fund_name", "aum", "nav", "strategy"],
            }
        },
        "required": ["fund_data"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "form_pf_json": {"type": "object"},
            "filing_frequency": {"type": "string"},
            "large_adviser": {"type": "boolean"},
            "systemic_risk_flags": {"type": "array", "items": {"type": "string"}},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": [
            "form_pf_json",
            "filing_frequency",
            "large_adviser",
            "systemic_risk_flags",
            "status",
            "timestamp",
        ],
    },
}

# Form PF thresholds (SEC Rule 204(b)-1, as amended 2023)
_LARGE_ADVISER_HEDGE_AUM = 1_500_000_000        # $1.5B for hedge fund advisers
_LARGE_ADVISER_LIQUIDITY_AUM = 1_000_000_000    # $1.0B for liquidity fund advisers
_LARGE_ADVISER_PE_AUM = 2_000_000_000           # $2.0B for PE advisers
_ALL_ADVISERS_THRESHOLD = 150_000_000           # $150M: must file Form PF at all

# Qualifying hedge fund: NAV >= $500M (Section 2 reporting)
_QUALIFYING_HEDGE_FUND_NAV = 500_000_000

# Leverage systemic risk threshold
_HIGH_LEVERAGE_RATIO = 10.0   # Gross leverage > 10x triggers systemic flag
_CONCENTRATION_PCT = 50.0     # Single position > 50% NAV


def sec_form_pf_compiler(fund_data: dict[str, Any]) -> dict[str, Any]:
    """Compile SEC Form PF data and determine filing obligations.

    Evaluates adviser-level AUM to determine Large Adviser status and
    quarterly vs. annual filing frequency. Generates a structured Form PF
    Section 1 payload and, for qualifying hedge funds, a Section 2 payload.
    Flags systemic risk indicators per Dodd-Frank and SEC guidance.

    Args:
        fund_data: Dictionary with fund identification, financials, strategy,
            leverage, investor data, and top portfolio positions.

    Returns:
        Dictionary with keys:
            status (str): "success" or "error".
            form_pf_json (dict): Structured payload for PFRD submission.
            filing_frequency (str): "quarterly" or "annually".
            large_adviser (bool): Whether adviser meets Large Adviser threshold.
            systemic_risk_flags (list[str]): Detected systemic risk concerns.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        fund_name: str = str(fund_data.get("fund_name", ""))
        aum: float = float(fund_data.get("aum", 0))
        nav: float = float(fund_data.get("nav", 0))
        strategy: str = str(fund_data.get("strategy", "other")).lower().replace(" ", "_")
        leverage_ratio: float = float(fund_data.get("leverage_ratio", 1.0))
        investor_count: int = int(fund_data.get("investor_count", 0))
        redemption_terms: str = str(fund_data.get("redemption_terms", "locked_up")).lower()
        top_positions: list[dict] = fund_data.get("top_positions", [])
        liquidity_stress_tested: bool = bool(fund_data.get("liquidity_stress_tested", False))
        prime_broker: str = str(fund_data.get("prime_broker", ""))
        domicile: str = str(fund_data.get("domicile", ""))

        systemic_risk_flags: list[str] = []

        # --- Filing Obligation Check ---
        # Advisers with RAUM < $150M are exempt from Form PF
        if aum < _ALL_ADVISERS_THRESHOLD:
            return {
                "status": "success",
                "data": {
                    "form_pf_json": {},
                    "filing_frequency": "exempt",
                    "large_adviser": False,
                    "systemic_risk_flags": [],
                    "reason": (
                        f"RAUM ${aum:,.0f} is below the $150M Form PF filing threshold. "
                        "No Form PF obligation (SEC Rule 204(b)-1(b))."
                    ),
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # --- Large Adviser Determination ---
        large_adviser = False
        if strategy in {"hedge_fund"} and aum >= _LARGE_ADVISER_HEDGE_AUM:
            large_adviser = True
        elif strategy in {"liquidity_fund"} and aum >= _LARGE_ADVISER_LIQUIDITY_AUM:
            large_adviser = True
        elif strategy in {"private_equity"} and aum >= _LARGE_ADVISER_PE_AUM:
            large_adviser = True

        filing_frequency = "quarterly" if large_adviser else "annually"

        # --- Qualifying Hedge Fund (Section 2) ---
        is_qualifying_hedge_fund = strategy == "hedge_fund" and nav >= _QUALIFYING_HEDGE_FUND_NAV

        # --- Systemic Risk Assessment ---
        if leverage_ratio > _HIGH_LEVERAGE_RATIO:
            systemic_risk_flags.append(
                f"High leverage: gross leverage ratio {leverage_ratio:.1f}x exceeds 10x systemic "
                "risk threshold (Form PF Section 2, Question 25)"
            )

        for pos in top_positions:
            pct = float(pos.get("pct_of_nav", 0))
            asset_class = pos.get("asset_class", "Unknown")
            if pct > _CONCENTRATION_PCT:
                systemic_risk_flags.append(
                    f"Concentration risk: '{asset_class}' position represents {pct:.1f}% of NAV "
                    f"(exceeds 50% concentration threshold)"
                )

        # Redemption liquidity mismatch risk
        if redemption_terms in {"daily", "monthly_30_day_notice"} and strategy == "hedge_fund":
            illiquid_positions = [
                p for p in top_positions
                if p.get("asset_class", "").lower() in {
                    "real_estate", "private_credit", "private_equity", "infrastructure", "art"
                }
            ]
            if illiquid_positions:
                systemic_risk_flags.append(
                    f"Liquidity mismatch: fund offers {redemption_terms} redemptions but holds "
                    f"{len(illiquid_positions)} illiquid position class(es) — "
                    "potential run risk (Form PF Section 1, Question 21)"
                )

        if not liquidity_stress_tested and strategy == "hedge_fund":
            systemic_risk_flags.append(
                "No liquidity stress testing performed. SEC expects quarterly stress tests "
                "for hedge funds above $500M NAV (Form PF Section 2, Question 27)"
            )

        # --- Form PF Section 1 (All advisers filing Form PF) ---
        section_1 = {
            "section": "Section 1 — Basic Information",
            "q1_fund_name": fund_name,
            "q2_fund_type": _map_strategy_to_form_pf_type(strategy),
            "q3_domicile": domicile,
            "q4_nav_usd": nav,
            "q5_raum_usd": aum,
            "q6_gross_leverage_ratio": leverage_ratio,
            "q7_investor_count": investor_count,
            "q8_redemption_terms": redemption_terms,
            "q9_prime_broker": prime_broker,
            "q10_strategy": strategy,
            "q11_liquidity_stress_tested": liquidity_stress_tested,
        }

        # --- Form PF Section 2 (Qualifying hedge funds only) ---
        section_2 = {}
        if is_qualifying_hedge_fund:
            total_notional = sum(float(p.get("notional_usd", 0)) for p in top_positions)
            section_2 = {
                "section": "Section 2 — Qualifying Hedge Funds",
                "q20_total_notional_exposure_usd": total_notional,
                "q21_redemption_terms": redemption_terms,
                "q22_investor_concentration": _compute_investor_concentration(investor_count),
                "q23_gross_leverage": leverage_ratio,
                "q24_net_leverage": leverage_ratio * 0.6,  # Approximation: net ~ 60% of gross
                "q25_position_concentration": [
                    {
                        "asset_class": p.get("asset_class"),
                        "notional_usd": p.get("notional_usd"),
                        "pct_of_nav": p.get("pct_of_nav"),
                    }
                    for p in top_positions
                ],
                "q27_liquidity_stress_tested": liquidity_stress_tested,
                "systemic_risk_flags": systemic_risk_flags,
            }

        form_pf_json = {
            "form_type": "Form PF",
            "filing_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "reporting_period_end": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "large_adviser": large_adviser,
            "filing_frequency": filing_frequency,
            "section_1": section_1,
            "section_2": section_2 if is_qualifying_hedge_fund else None,
            "regulations": [
                "Dodd-Frank Wall Street Reform Act Section 404",
                "SEC Rule 204(b)-1 — Form PF reporting",
                "SEC Form PF Instructions (2023 amendments effective December 2023)",
                "Investment Advisers Act Section 204",
            ],
        }

        result = {
            "form_pf_json": form_pf_json,
            "filing_frequency": filing_frequency,
            "large_adviser": large_adviser,
            "is_qualifying_hedge_fund": is_qualifying_hedge_fund,
            "systemic_risk_flags": systemic_risk_flags,
            "section_2_required": is_qualifying_hedge_fund,
            "deadline": (
                "60 days after fiscal quarter end (quarterly filers) or "
                "120 days after fiscal year end (annual filers)"
            ),
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"sec_form_pf_compiler failed: {e}")
        _log_lesson(f"sec_form_pf_compiler: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _map_strategy_to_form_pf_type(strategy: str) -> str:
    """Map internal strategy name to Form PF fund type label.

    Args:
        strategy: Internal strategy string.

    Returns:
        Form PF fund type label string.
    """
    mapping = {
        "hedge_fund": "Hedge Fund",
        "liquidity_fund": "Liquidity Fund",
        "private_equity": "Private Equity Fund",
        "real_estate": "Real Estate Fund",
        "securitised_asset": "Securitised Asset Fund",
        "other": "Other Private Fund",
    }
    return mapping.get(strategy, "Other Private Fund")


def _compute_investor_concentration(investor_count: int) -> str:
    """Assess investor concentration risk from investor count.

    Args:
        investor_count: Number of investors in the fund.

    Returns:
        Concentration risk descriptor string.
    """
    if investor_count <= 5:
        return "highly_concentrated"
    if investor_count <= 25:
        return "concentrated"
    if investor_count <= 100:
        return "moderate"
    return "diversified"


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
