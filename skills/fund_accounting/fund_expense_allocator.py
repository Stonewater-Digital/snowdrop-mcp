"""
Executive Summary: Allocates fund-level expenses across sub-funds using pro-rata NAV, equal split, or committed-capital weighting.

Inputs: total_expenses (float), sub_funds (list[dict]: name str, allocation_basis str, basis_value float)
Outputs: dict with allocations (list[dict]: fund_name, allocated_amount, pct_of_total)
MCP Tool Name: fund_expense_allocator
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "fund_expense_allocator",
    "description": (
        "Allocates a total expense amount across sub-funds based on their chosen allocation basis: "
        "'pro_rata_nav' (weighted by current NAV), 'equal' (split evenly), or "
        "'committed_capital' (weighted by LP capital commitments). "
        "Returns dollar allocations and percentage shares for each sub-fund."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_expenses": {
                "type": "number",
                "description": "Total expense amount in dollars to be allocated across sub-funds"
            },
            "sub_funds": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "allocation_basis": {
                            "type": "string",
                            "enum": ["pro_rata_nav", "equal", "committed_capital"],
                            "description": "Methodology for allocating expenses to this sub-fund"
                        },
                        "basis_value": {
                            "type": "number",
                            "description": "NAV or committed capital in dollars (ignored for 'equal' basis)"
                        }
                    },
                    "required": ["name", "allocation_basis", "basis_value"]
                },
                "minItems": 1,
                "description": "List of sub-funds with their allocation methodology and basis values"
            }
        },
        "required": ["total_expenses", "sub_funds"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "allocations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "fund_name": {"type": "string"},
                        "allocation_basis": {"type": "string"},
                        "basis_value": {"type": "number"},
                        "allocated_amount": {"type": "number"},
                        "pct_of_total": {"type": "number"}
                    }
                }
            },
            "total_allocated": {"type": "number"},
            "rounding_residual": {"type": "number"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["allocations", "total_allocated", "status", "timestamp"]
    }
}

_VALID_BASES = {"pro_rata_nav", "equal", "committed_capital"}


def _compute_weights(sub_funds: list[dict]) -> list[float]:
    """Compute allocation weight for each sub-fund.

    Funds on 'equal' basis each receive weight = 1. Funds on 'pro_rata_nav'
    or 'committed_capital' basis use their basis_value as weight. All weights
    are then normalized to sum to 1.0.

    Note: Mixed-basis scenarios are handled by normalizing the raw weights,
    meaning an 'equal' fund competes as weight=1 against value-weighted peers.
    For strict mixed-basis isolation, pre-group expenses by basis type upstream.

    Args:
        sub_funds: List of sub-fund dicts with 'allocation_basis' and 'basis_value'.

    Returns:
        List of normalized weights (floats) summing to 1.0, one per sub-fund.

    Raises:
        ValueError: If any basis_value is negative, or if total weight is zero.
    """
    raw_weights: list[float] = []
    for sf in sub_funds:
        basis = sf["allocation_basis"]
        val = float(sf["basis_value"])
        if basis == "equal":
            raw_weights.append(1.0)
        elif basis in ("pro_rata_nav", "committed_capital"):
            if val < 0:
                raise ValueError(
                    f"Sub-fund '{sf['name']}' has negative basis_value {val} "
                    f"for '{basis}' allocation — basis values must be non-negative"
                )
            raw_weights.append(val)
        else:
            raise ValueError(
                f"Unknown allocation_basis '{basis}' for sub-fund '{sf['name']}'. "
                f"Valid options: {_VALID_BASES}"
            )

    total_weight = sum(raw_weights)
    if total_weight == 0:
        raise ValueError(
            "Total allocation weight is zero — all basis_values are 0. "
            "Cannot distribute expenses with zero total weight."
        )

    return [w / total_weight for w in raw_weights]


def fund_expense_allocator(**kwargs: Any) -> dict:
    """Allocate a total expense pool across sub-funds using their specified allocation basis.

    Supports three allocation methods:
    - pro_rata_nav: Each sub-fund's share proportional to its current NAV.
    - committed_capital: Each sub-fund's share proportional to LP commitments.
    - equal: Each sub-fund receives an identical share regardless of size.

    Rounding residual (if any) is reported but not redistributed to preserve
    exact transparency. The largest sub-fund implicitly absorbs rounding via
    the final sum check.

    Args:
        **kwargs: Keyword arguments containing:
            total_expenses (float): Total dollars to allocate.
            sub_funds (list[dict]): Each dict must have:
                - name (str): Sub-fund identifier
                - allocation_basis (str): 'pro_rata_nav' | 'equal' | 'committed_capital'
                - basis_value (float): NAV or commitment size (ignored for 'equal')

    Returns:
        dict: Contains:
            - status (str): 'success' or 'error'
            - data (dict):
                - allocations (list[dict]): Per sub-fund allocations with pct_of_total
                - total_allocated (float): Sum of all allocations (should match total_expenses)
                - rounding_residual (float): Floating point difference from total_expenses
            - timestamp (str): ISO 8601 UTC timestamp
    """
    try:
        total_expenses: float = float(kwargs.get("total_expenses", 0))
        sub_funds: list[dict] = kwargs.get("sub_funds", [])

        if total_expenses < 0:
            raise ValueError(f"total_expenses must be non-negative, got {total_expenses}")
        if not sub_funds:
            raise ValueError("sub_funds list is empty — at least one sub-fund is required")

        weights = _compute_weights(sub_funds)

        allocations: list[dict] = []
        running_total = 0.0

        for sf, weight in zip(sub_funds, weights):
            allocated = round(total_expenses * weight, 6)
            pct = round(weight * 100, 6)
            running_total += allocated
            allocations.append({
                "fund_name": sf["name"],
                "allocation_basis": sf["allocation_basis"],
                "basis_value": float(sf["basis_value"]),
                "weight": round(weight, 8),
                "allocated_amount": allocated,
                "pct_of_total": pct,
            })

        rounding_residual = round(running_total - total_expenses, 10)

        result = {
            "allocations": allocations,
            "total_allocated": round(running_total, 6),
            "total_expenses_input": total_expenses,
            "rounding_residual": rounding_residual,
            "n_sub_funds": len(sub_funds),
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"fund_expense_allocator failed: {e}")
        _log_lesson(f"fund_expense_allocator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the shared lessons log.

    Args:
        message: The lesson or error description to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")
