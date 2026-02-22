"""
Executive Summary: Models equity dilution across funding rounds, tracking ownership percentages per stakeholder with option pool.

Inputs: rounds (list[dict]: series, amount, pre_money), option_pool_pct (float)
Outputs: dict with ownership_table (list[dict] per stakeholder per round), dilution_per_round (list)
MCP Tool Name: cap_table_simulator
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "cap_table_simulator",
    "description": "Models equity dilution across funding rounds, tracking ownership percentages per stakeholder with option pool.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "rounds": {
                "type": "array",
                "description": "List of funding rounds",
                "items": {
                    "type": "object",
                    "properties": {
                        "series": {"type": "string", "description": "Round name (e.g. Seed, Series A)"},
                        "amount": {"type": "number", "description": "Investment amount in dollars"},
                        "pre_money": {"type": "number", "description": "Pre-money valuation in dollars"},
                    },
                    "required": ["series", "amount", "pre_money"],
                },
            },
            "option_pool_pct": {
                "type": "number",
                "description": "Option pool as a fraction of post-money (e.g. 0.10 for 10%)",
            },
        },
        "required": ["rounds", "option_pool_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "ownership_table": {"type": "array"},
            "dilution_per_round": {"type": "array"},
            "final_cap_table": {"type": "object"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["ownership_table", "dilution_per_round", "status", "timestamp"],
    },
}

_SHARES_PER_DOLLAR = 1.0  # 1 share = $1 face value; price adjusts by round


def cap_table_simulator(
    rounds: list[dict[str, Any]],
    option_pool_pct: float,
    **kwargs: Any,
) -> dict:
    """Simulates cap table evolution across multiple funding rounds.

    For each round:
    - post_money = pre_money + amount
    - new_investor_pct = amount / post_money
    - option_pool carved out of post-money
    - founders and prior investors diluted proportionally

    Stakeholders tracked: founders (start at 100%), option_pool, and each
    investor series (Seed, Series_A, etc.).

    Args:
        rounds: List of round dicts with keys: series (str), amount (float),
            pre_money (float).
        option_pool_pct: Option pool as fraction of post-money equity.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Contains ownership_table (list of per-round snapshots),
              dilution_per_round (list of dilution metrics), final_cap_table
              (dict of final ownership fractions), status, and timestamp.
    """
    try:
        if not rounds:
            raise ValueError("rounds list cannot be empty")
        if not (0.0 <= option_pool_pct < 1.0):
            raise ValueError("option_pool_pct must be between 0 and 1 (exclusive)")

        # Ownership fractions (sum to 1.0 at each round end)
        ownership: dict[str, float] = {"founders": 1.0}
        ownership_table: list[dict] = []
        dilution_per_round: list[dict] = []

        for rnd in rounds:
            series = rnd["series"]
            amount = float(rnd["amount"])
            pre_money = float(rnd["pre_money"])

            if pre_money <= 0:
                raise ValueError(f"pre_money must be positive for round {series}")
            if amount <= 0:
                raise ValueError(f"amount must be positive for round {series}")

            post_money = pre_money + amount
            new_investor_pct = amount / post_money

            # Option pool is carved from post-money (pre-money shuffle is common
            # but we apply it as a flat post-money allocation for simplicity)
            # Total new allocations: new investor + any option pool expansion
            # Existing holders diluted by (1 - new_investor_pct - option_pool_pct)
            retention_factor = 1.0 - new_investor_pct - option_pool_pct
            if retention_factor < 0:
                raise ValueError(
                    f"Round {series}: new_investor_pct ({new_investor_pct:.2%}) + "
                    f"option_pool_pct ({option_pool_pct:.2%}) exceeds 1.0"
                )

            founders_before = ownership.get("founders", 0.0)

            # Dilute all existing holders
            new_ownership: dict[str, float] = {}
            for holder, pct in ownership.items():
                new_ownership[holder] = pct * retention_factor

            # Add new investor and option pool
            new_ownership[series] = new_investor_pct
            new_ownership["option_pool"] = new_ownership.get("option_pool", 0.0) + option_pool_pct

            ownership = new_ownership

            snapshot = {
                "round": series,
                "pre_money": round(pre_money, 2),
                "amount_raised": round(amount, 2),
                "post_money": round(post_money, 2),
                "ownership": {k: round(v, 6) for k, v in ownership.items()},
                "total_pct": round(sum(ownership.values()), 6),
            }
            ownership_table.append(snapshot)

            founders_after = ownership.get("founders", 0.0)
            founder_dilution = founders_before - founders_after if founders_before > 0 else 0.0
            dilution_per_round.append({
                "round": series,
                "founders_before": round(founders_before, 6),
                "founders_after": round(founders_after, 6),
                "founder_dilution_pct": round(founder_dilution, 6),
                "new_investor_pct": round(new_investor_pct, 6),
                "option_pool_pct_added": round(option_pool_pct, 6),
            })

        final_cap_table = {k: round(v, 6) for k, v in ownership.items()}

        result = {
            "ownership_table": ownership_table,
            "dilution_per_round": dilution_per_round,
            "final_cap_table": final_cap_table,
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        logger.error(f"cap_table_simulator failed: {e}")
        _log_lesson(f"cap_table_simulator: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Appends an error lesson to the lessons log.

    Args:
        message: The lesson message to log.
    """
    os.makedirs("logs", exist_ok=True)
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
