"""
Executive Summary: Simulates sovereign fund inflation protection by modeling real portfolio returns across multiple inflation scenarios and suggesting optimal allocation shifts.
Inputs: portfolio (dict of asset class percentages), inflation_scenarios (list[float]), fund_value (float)
Outputs: scenario_results (list[dict]), optimal_allocation_shift (dict)
MCP Tool Name: inflation_hedging_simulator
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "inflation_hedging_simulator",
    "description": "Models sovereign fund real returns across inflation scenarios and recommends allocation shifts for inflation protection.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio": {
                "type": "object",
                "description": "Asset class allocation as percentages (must sum to ~100)",
                "properties": {
                    "nominal_bonds_pct": {"type": "number"},
                    "tips_pct": {"type": "number"},
                    "gold_pct": {"type": "number"},
                    "commodities_pct": {"type": "number"},
                    "real_estate_pct": {"type": "number"},
                    "crypto_pct": {"type": "number"}
                }
            },
            "inflation_scenarios": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of annual inflation rates to simulate (e.g. [0.02, 0.05, 0.10])"
            },
            "fund_value": {"type": "number", "description": "Initial sovereign fund value in USD"}
        },
        "required": ["portfolio", "inflation_scenarios", "fund_value"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "scenario_results": {"type": "array"},
                    "optimal_allocation_shift": {"type": "object"}
                }
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "data", "timestamp"]
    }
}

# Asset class real return models: real_return = nominal_return - inflation * sensitivity
# Tuple: (base_nominal_return, inflation_sensitivity, inflation_beta)
# inflation_beta: multiplier on inflation for hedging assets (>1 = hedges above inflation)
# Model: real_return = base_nominal - inflation + (inflation_beta - 1) * inflation
ASSET_CLASS_PARAMS: dict[str, dict[str, float]] = {
    "nominal_bonds_pct": {
        "label": "Nominal Bonds",
        "base_nominal": 0.04,     # 4% nominal yield
        "inflation_beta": 0.0,    # No inflation pass-through; worst in high-inflation
        "description": "Fixed coupon; real return erodes 1:1 with unexpected inflation"
    },
    "tips_pct": {
        "label": "TIPS / Inflation-Linked Bonds",
        "base_nominal": 0.015,    # 1.5% real yield floor
        "inflation_beta": 1.0,    # Principal adjusts 1:1 with CPI
        "description": "Principal indexed to CPI; real yield protected but modest"
    },
    "gold_pct": {
        "label": "Gold",
        "base_nominal": 0.03,     # Long-run nominal ~3%
        "inflation_beta": 1.15,   # Slight outperformance vs inflation historically
        "description": "Store of value; outperforms moderately above CPI long-term"
    },
    "commodities_pct": {
        "label": "Commodities",
        "base_nominal": 0.04,
        "inflation_beta": 1.3,    # Strong hedge; commodities often drive CPI
        "description": "Direct hedge; often leads CPI; volatile but effective"
    },
    "real_estate_pct": {
        "label": "Real Estate / REITs",
        "base_nominal": 0.055,    # 5.5% nominal (income + appreciation)
        "inflation_beta": 1.1,    # Rents tend to track inflation
        "description": "Income-generating; rents index to inflation over time"
    },
    "crypto_pct": {
        "label": "Crypto / Digital Assets",
        "base_nominal": 0.20,     # High expected nominal return
        "inflation_beta": 0.8,    # Partial hedge; high volatility, correlation uncertain
        "description": "Speculative store of value; limited inflation history; high vol"
    },
}


def _compute_real_return(asset_key: str, inflation: float) -> float:
    """Compute expected real return for an asset class at a given inflation rate.

    Uses the model: real_return = base_nominal - inflation * (1 - inflation_beta)
    For assets with inflation_beta >= 1.0, the principal/income adjusts with inflation,
    so real return is approximately base_nominal.
    For nominal bonds (beta=0), real_return degrades by full inflation.

    Args:
        asset_key: Key into ASSET_CLASS_PARAMS (e.g. 'tips_pct').
        inflation: Annual inflation rate as a decimal (e.g. 0.05 for 5%).

    Returns:
        float: Expected real return as a decimal.
    """
    params = ASSET_CLASS_PARAMS[asset_key]
    base = params["base_nominal"]
    beta = params["inflation_beta"]
    # Effective nominal return considering inflation pass-through
    effective_nominal = base + beta * inflation
    real_return = effective_nominal - inflation
    return real_return


def inflation_hedging_simulator(
    portfolio: dict[str, float],
    inflation_scenarios: list[float],
    fund_value: float,
    **kwargs: Any
) -> dict[str, Any]:
    """Simulate sovereign fund performance across inflation scenarios.

    For each inflation scenario, computes the portfolio's weighted real and
    nominal return by summing each asset class's contribution. Identifies
    the scenario where the portfolio is most vulnerable (lowest real return)
    and recommends an optimal allocation shift toward inflation-hedging assets.

    Args:
        portfolio: Dictionary of asset class percentage allocations. Keys:
            'nominal_bonds_pct', 'tips_pct', 'gold_pct', 'commodities_pct',
            'real_estate_pct', 'crypto_pct'. Values are percentages (0–100).
            Should sum to approximately 100.
        inflation_scenarios: List of annual inflation rates as decimals
            (e.g. [0.02, 0.05, 0.10, 0.15]).
        fund_value: Initial fund value in USD.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Standard Snowdrop response envelope with keys:
            - status (str): 'success' or 'error'.
            - data (dict): Results including scenario_results (list of dicts
              with inflation_rate, real_return, nominal_return, value_after_1yr,
              real_value_after_1yr, per_asset_breakdown), optimal_allocation_shift
              (dict of recommended changes), and portfolio_summary.
            - timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        fund_value = float(fund_value)
        if fund_value <= 0:
            raise ValueError("fund_value must be positive")
        if not inflation_scenarios:
            raise ValueError("inflation_scenarios must be non-empty")

        # Normalize portfolio: convert from pct to weight (0.0–1.0)
        known_keys = set(ASSET_CLASS_PARAMS.keys())
        weights: dict[str, float] = {}
        total_alloc = 0.0
        for k in known_keys:
            pct = float(portfolio.get(k, 0.0))
            weights[k] = pct / 100.0
            total_alloc += pct

        if abs(total_alloc - 100.0) > 5.0:
            logger.warning(
                f"Portfolio allocations sum to {total_alloc:.1f}% (expected ~100%); proceeding with normalization"
            )
            # Normalize to 1.0
            if total_alloc > 0:
                for k in weights:
                    weights[k] = weights[k] / (total_alloc / 100.0)

        scenario_results: list[dict[str, Any]] = []

        for inflation in sorted(inflation_scenarios):
            inflation = float(inflation)
            weighted_real = 0.0
            weighted_nominal = 0.0
            per_asset: list[dict[str, Any]] = []

            for asset_key, weight in weights.items():
                if weight == 0.0:
                    continue
                params = ASSET_CLASS_PARAMS[asset_key]
                real_ret = _compute_real_return(asset_key, inflation)
                nominal_ret = real_ret + inflation
                contribution_real = weight * real_ret
                contribution_nominal = weight * nominal_ret

                weighted_real += contribution_real
                weighted_nominal += contribution_nominal

                per_asset.append({
                    "asset": params["label"],
                    "weight_pct": round(weight * 100, 4),
                    "real_return": round(real_ret * 100, 4),
                    "nominal_return": round(nominal_ret * 100, 4),
                    "contribution_to_real_return": round(contribution_real * 100, 6),
                })

            nominal_value = round(fund_value * (1 + weighted_nominal), 2)
            real_value = round(fund_value * (1 + weighted_real), 2)

            scenario_results.append({
                "inflation_rate": inflation,
                "inflation_rate_pct": round(inflation * 100, 2),
                "real_return": round(weighted_real, 6),
                "real_return_pct": round(weighted_real * 100, 4),
                "nominal_return": round(weighted_nominal, 6),
                "nominal_return_pct": round(weighted_nominal * 100, 4),
                "value_after_1yr": nominal_value,
                "real_value_after_1yr": real_value,
                "purchasing_power_preserved": weighted_real >= 0,
                "per_asset_breakdown": per_asset,
            })

        # Optimal allocation shift analysis
        # Find worst-performing scenario (highest inflation in list as proxy)
        max_inflation = max(float(s) for s in inflation_scenarios)
        worst_result = next(r for r in scenario_results if r["inflation_rate"] == max_inflation)

        # Calculate current inflation-hedge ratio
        hedge_assets = {"tips_pct", "gold_pct", "commodities_pct", "real_estate_pct"}
        current_hedge_pct = sum(float(portfolio.get(k, 0.0)) for k in hedge_assets)
        current_nominal_pct = float(portfolio.get("nominal_bonds_pct", 0.0))

        # Recommend shift if real return is negative in worst scenario
        optimal_allocation_shift: dict[str, Any] = {}
        if worst_result["real_return"] < 0:
            shift_from_nominal = min(current_nominal_pct, 20.0)  # Max 20ppt shift
            shift_to_tips = round(shift_from_nominal * 0.5, 2)
            shift_to_gold = round(shift_from_nominal * 0.3, 2)
            shift_to_commodities = round(shift_from_nominal * 0.2, 2)

            optimal_allocation_shift = {
                "action": "REDUCE_NOMINAL_BONDS",
                "rationale": f"Portfolio loses real value at {max_inflation*100:.0f}% inflation; shift toward inflation-linked assets",
                "reduce_nominal_bonds_by_ppt": shift_from_nominal,
                "increase_tips_by_ppt": shift_to_tips,
                "increase_gold_by_ppt": shift_to_gold,
                "increase_commodities_by_ppt": shift_to_commodities,
                "projected_real_return_improvement_ppt": round(
                    shift_from_nominal / 100 * (
                        _compute_real_return("tips_pct", max_inflation) -
                        _compute_real_return("nominal_bonds_pct", max_inflation)
                    ) * 100, 4
                ),
            }
        else:
            optimal_allocation_shift = {
                "action": "NO_CHANGE_REQUIRED",
                "rationale": "Portfolio preserves real value across all tested inflation scenarios",
                "current_hedge_pct": current_hedge_pct,
            }

        result: dict[str, Any] = {
            "scenario_results": scenario_results,
            "optimal_allocation_shift": optimal_allocation_shift,
            "portfolio_summary": {
                "total_allocation_pct": round(total_alloc, 2),
                "inflation_hedge_pct": round(current_hedge_pct, 2),
                "nominal_bonds_pct": float(portfolio.get("nominal_bonds_pct", 0.0)),
                "fund_value_initial": fund_value,
            },
            "scenarios_tested": len(inflation_scenarios),
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"inflation_hedging_simulator failed: {e}")
        _log_lesson(f"inflation_hedging_simulator: {e}")
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
