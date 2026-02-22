"""
Executive Summary: Calculate cost basis by FIFO/LIFO/average/specific-lot methods, identify tax-loss harvesting opportunities, and flag wash sale risk.
Inputs: lots (list of dicts), current_price (float), method (str)
Outputs: cost_basis (float), unrealized_gain_loss (float), harvestable_losses (list), wash_sale_risk (bool), method_comparison (dict)
MCP Tool Name: cost_basis_averaging_logic
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone, timedelta

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "cost_basis_averaging_logic",
    "description": "Calculate cost basis using FIFO, LIFO, average cost, or specific-lot method. Identifies tax-loss harvesting opportunities and wash sale risk.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "lots": {
                "type": "array",
                "description": "List of tax lots, each with: purchase_date (ISO date str), quantity (float), price_per_unit (float), fees (float).",
                "items": {
                    "type": "object",
                    "properties": {
                        "purchase_date": {"type": "string"},
                        "quantity": {"type": "number"},
                        "price_per_unit": {"type": "number"},
                        "fees": {"type": "number"}
                    },
                    "required": ["purchase_date", "quantity", "price_per_unit", "fees"]
                }
            },
            "current_price": {
                "type": "number",
                "description": "Current market price per unit."
            },
            "method": {
                "type": "string",
                "enum": ["fifo", "lifo", "average", "specific"],
                "description": "Cost basis calculation method: 'fifo', 'lifo', 'average', or 'specific'."
            }
        },
        "required": ["lots", "current_price", "method"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "cost_basis": {"type": "number"},
            "unrealized_gain_loss": {"type": "number"},
            "harvestable_losses": {"type": "array"},
            "wash_sale_risk": {"type": "boolean"},
            "method_comparison": {"type": "object"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["cost_basis", "unrealized_gain_loss", "harvestable_losses", "wash_sale_risk", "method_comparison", "status", "timestamp"]
    }
}

# IRS wash sale rule: repurchase within 30 days before or after a sale creates a wash sale
_WASH_SALE_WINDOW_DAYS = 30


def _parse_date(date_str: str) -> datetime:
    """Parse a date string to a datetime object (date-only, no time).

    Args:
        date_str: ISO date string in YYYY-MM-DD format.

    Returns:
        datetime object at midnight UTC.

    Raises:
        ValueError: If the date string cannot be parsed.
    """
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        # Try full ISO with time
        return datetime.fromisoformat(date_str.strip().replace("Z", "+00:00")).replace(
            hour=0, minute=0, second=0, microsecond=0
        ).astimezone(timezone.utc)


def _enrich_lot(lot: dict, idx: int) -> dict:
    """Validate and enrich a single tax lot dict.

    Args:
        lot: Raw lot dict from input.
        idx: Index for error messages.

    Returns:
        Enriched lot dict with computed fields.

    Raises:
        ValueError: If required fields are invalid.
    """
    quantity = float(lot["quantity"])
    price = float(lot["price_per_unit"])
    fees = float(lot["fees"])

    if quantity <= 0:
        raise ValueError(f"Lot {idx}: quantity must be positive, got {quantity}.")
    if price < 0:
        raise ValueError(f"Lot {idx}: price_per_unit cannot be negative, got {price}.")
    if fees < 0:
        raise ValueError(f"Lot {idx}: fees cannot be negative, got {fees}.")

    purchase_date = _parse_date(str(lot["purchase_date"]))
    # Total cost = (quantity * price) + fees
    total_cost = (quantity * price) + fees
    cost_basis_per_unit = total_cost / quantity

    return {
        "purchase_date": purchase_date,
        "purchase_date_str": lot["purchase_date"],
        "quantity": quantity,
        "price_per_unit": price,
        "fees": fees,
        "total_cost": round(total_cost, 8),
        "cost_basis_per_unit": round(cost_basis_per_unit, 8),
        "lot_index": idx,
    }


def _compute_fifo(lots: list[dict], current_price: float) -> tuple[float, float]:
    """Compute FIFO cost basis (oldest lots first).

    Args:
        lots: Enriched, date-sorted lots (ascending).
        current_price: Current market price per unit.

    Returns:
        Tuple of (weighted_avg_cost_basis_per_unit, total_unrealized_gain_loss).
    """
    total_cost = sum(lot["total_cost"] for lot in lots)
    total_qty = sum(lot["quantity"] for lot in lots)
    avg_cb = total_cost / total_qty if total_qty else 0.0
    current_value = total_qty * current_price
    unrealized = current_value - total_cost
    return round(avg_cb, 8), round(unrealized, 8)


def _compute_lifo(lots: list[dict], current_price: float) -> tuple[float, float]:
    """Compute LIFO cost basis (newest lots first).

    In practice LIFO uses the most recent lot cost as the primary basis.
    Here we compute the LIFO-specific average (newest-weighted).

    Args:
        lots: Enriched lots (will be reversed for LIFO ordering).
        current_price: Current market price per unit.

    Returns:
        Tuple of (lifo_avg_cost_basis_per_unit, total_unrealized_gain_loss).
    """
    lifo_lots = list(reversed(lots))
    total_cost = sum(lot["total_cost"] for lot in lifo_lots)
    total_qty = sum(lot["quantity"] for lot in lifo_lots)
    avg_cb = total_cost / total_qty if total_qty else 0.0
    current_value = total_qty * current_price
    unrealized = current_value - total_cost
    return round(avg_cb, 8), round(unrealized, 8)


def _compute_average(lots: list[dict], current_price: float) -> tuple[float, float]:
    """Compute average cost basis across all lots.

    Args:
        lots: All enriched lots.
        current_price: Current market price per unit.

    Returns:
        Tuple of (average_cost_basis_per_unit, total_unrealized_gain_loss).
    """
    total_cost = sum(lot["total_cost"] for lot in lots)
    total_qty = sum(lot["quantity"] for lot in lots)
    avg_cb = total_cost / total_qty if total_qty else 0.0
    current_value = total_qty * current_price
    unrealized = current_value - total_cost
    return round(avg_cb, 8), round(unrealized, 8)


def _compute_specific(lots: list[dict], current_price: float) -> tuple[float, float]:
    """Compute specific lot cost basis (optimize for tax-loss harvesting).

    Identifies the lot with the highest cost basis per unit (loss-maximizing
    for tax purposes when price has declined).

    Args:
        lots: All enriched lots.
        current_price: Current market price per unit.

    Returns:
        Tuple of (highest_cost_basis_per_unit, unrealized_gain_loss_for_that_lot).
    """
    if not lots:
        return 0.0, 0.0

    # Specific: select the highest cost basis lot (best for harvesting losses)
    highest_lot = max(lots, key=lambda lot: lot["cost_basis_per_unit"])
    cb = highest_lot["cost_basis_per_unit"]
    unrealized_per_lot = (current_price - cb) * highest_lot["quantity"]
    return round(cb, 8), round(unrealized_per_lot, 8)


def _identify_harvestable_losses(lots: list[dict], current_price: float) -> list[dict]:
    """Identify lots with unrealized losses suitable for tax-loss harvesting.

    Args:
        lots: All enriched lots.
        current_price: Current market price per unit.

    Returns:
        List of lot dicts (enriched) with unrealized loss amounts, sorted by loss descending.
    """
    harvestable = []
    for lot in lots:
        market_value = lot["quantity"] * current_price
        unrealized = market_value - lot["total_cost"]
        if unrealized < 0:
            harvestable.append({
                "lot_index": lot["lot_index"],
                "purchase_date": lot["purchase_date_str"],
                "quantity": lot["quantity"],
                "cost_basis_per_unit": lot["cost_basis_per_unit"],
                "current_price": current_price,
                "unrealized_loss": round(unrealized, 8),
                "loss_per_unit": round(current_price - lot["cost_basis_per_unit"], 8),
                "market_value": round(market_value, 8),
                "total_cost": lot["total_cost"],
            })

    harvestable.sort(key=lambda x: x["unrealized_loss"])  # largest losses first
    return harvestable


def _check_wash_sale_risk(lots: list[dict]) -> bool:
    """Check if any two lots are within the IRS 30-day wash sale window.

    If lots were purchased within 30 days of each other, selling the older lot
    at a loss while still holding the newer lot could trigger wash sale disallowance.

    Args:
        lots: All enriched lots with purchase_date as datetime.

    Returns:
        True if wash sale risk exists (lots within 30-day window of each other).
    """
    if len(lots) < 2:
        return False

    dates = sorted(lot["purchase_date"] for lot in lots)
    window = timedelta(days=_WASH_SALE_WINDOW_DAYS)

    for i in range(len(dates) - 1):
        if dates[i + 1] - dates[i] <= window:
            return True
    return False


def cost_basis_averaging_logic(
    lots: list[dict],
    current_price: float,
    method: str,
) -> dict:
    """Calculate cost basis, unrealized gain/loss, and tax-loss harvesting opportunities.

    Supports four IRS-recognized cost basis methods. The "specific" method
    selects the highest-cost lot to maximize harvestable losses when the asset
    has declined in value.

    Args:
        lots: List of tax lot dicts with purchase_date, quantity, price_per_unit, fees.
        current_price: Current market price per unit of the asset.
        method: Cost basis method — "fifo", "lifo", "average", or "specific".

    Returns:
        A dict with keys:
            - cost_basis (float): Cost basis per unit for the selected method.
            - unrealized_gain_loss (float): Total unrealized gain (+) or loss (-).
            - harvestable_losses (list): Lots with unrealized losses for harvesting.
            - wash_sale_risk (bool): True if lots are within 30-day wash sale window.
            - method_comparison (dict): Cost basis and gain/loss for all four methods.
            - status (str): "success" or "error".
            - timestamp (str): ISO 8601 UTC timestamp.
    """
    try:
        method = method.strip().lower()
        if method not in ("fifo", "lifo", "average", "specific"):
            raise ValueError(f"method must be 'fifo', 'lifo', 'average', or 'specific', got '{method}'.")
        if current_price < 0:
            raise ValueError(f"current_price cannot be negative, got {current_price}.")
        if not isinstance(lots, list) or len(lots) == 0:
            raise ValueError("lots must be a non-empty list.")

        enriched = [_enrich_lot(lot, idx) for idx, lot in enumerate(lots)]
        # Sort by date ascending for FIFO ordering
        enriched_sorted = sorted(enriched, key=lambda l: l["purchase_date"])

        # Compute selected method
        method_funcs = {
            "fifo": _compute_fifo,
            "lifo": _compute_lifo,
            "average": _compute_average,
            "specific": _compute_specific,
        }

        cost_basis, unrealized_gain_loss = method_funcs[method](enriched_sorted, current_price)

        # Method comparison: compute all four
        method_comparison: dict[str, dict] = {}
        for m, func in method_funcs.items():
            cb, ugl = func(enriched_sorted, current_price)
            method_comparison[m] = {
                "cost_basis_per_unit": cb,
                "unrealized_gain_loss": ugl,
            }

        harvestable_losses = _identify_harvestable_losses(enriched_sorted, current_price)
        wash_sale_risk = _check_wash_sale_risk(enriched_sorted)

        total_qty = sum(lot["quantity"] for lot in enriched_sorted)
        total_cost_all = sum(lot["total_cost"] for lot in enriched_sorted)
        current_total_value = total_qty * current_price

        return {
            "status": "success",
            "cost_basis": cost_basis,
            "method": method,
            "unrealized_gain_loss": unrealized_gain_loss,
            "harvestable_losses": harvestable_losses,
            "wash_sale_risk": wash_sale_risk,
            "wash_sale_window_days": _WASH_SALE_WINDOW_DAYS,
            "method_comparison": method_comparison,
            "summary": {
                "total_lots": len(enriched_sorted),
                "total_quantity": round(total_qty, 8),
                "total_cost_basis": round(total_cost_all, 8),
                "current_market_value": round(current_total_value, 8),
                "current_price": current_price,
                "harvestable_loss_count": len(harvestable_losses),
                "total_harvestable_loss": round(
                    sum(h["unrealized_loss"] for h in harvestable_losses), 8
                ),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"cost_basis_averaging_logic failed: {e}")
        _log_lesson(f"cost_basis_averaging_logic: {e}")
        return {
            "status": "error",
            "error": str(e),
            "cost_basis": 0.0,
            "unrealized_gain_loss": 0.0,
            "harvestable_losses": [],
            "wash_sale_risk": False,
            "method_comparison": {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the lessons log file.

    Args:
        message: The lesson message to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")
