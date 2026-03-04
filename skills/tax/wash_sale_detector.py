"""Detect potential wash sales in trading activity."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "wash_sale_detector",
    "description": "Flags loss sales with repurchases inside the 30-day wash window.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "transactions": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Transactions with asset, action, date, amount, price.",
            }
        },
        "required": ["transactions"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def wash_sale_detector(transactions: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Identify sales at a loss with matching repurchases +/-30 days."""
    try:
        if not transactions:
            raise ValueError("transactions cannot be empty")

        normalized = [_normalize_tx(tx) for tx in transactions]
        normalized.sort(key=lambda tx: tx["date"])
        inventory: dict[str, list[dict[str, float]]] = {}
        buy_dates: dict[str, list[datetime]] = {}
        for tx in normalized:
            if tx["action"] == "buy":
                inventory.setdefault(tx["asset"], []).append(
                    {"quantity": tx["amount"], "price": tx["price"], "date": tx["date"]}
                )
                buy_dates.setdefault(tx["asset"], []).append(tx["date"])

        flagged: list[dict[str, Any]] = []
        # reset inventory so FIFO is recalculated sequentially
        inventory = {asset: [] for asset in inventory}

        for tx in normalized:
            asset = tx["asset"]
            if tx["action"] == "buy":
                inventory.setdefault(asset, []).append(
                    {"quantity": tx["amount"], "price": tx["price"], "date": tx["date"]}
                )
                continue

            loss, cost_basis = _loss_from_sale(inventory.get(asset, []), tx)
            if loss >= 0:
                continue

            window = timedelta(days=30)
            sale_date = tx["date"]
            related_buys = [
                dt.isoformat()
                for dt in buy_dates.get(asset, [])
                if abs((dt - sale_date).days) <= window.days and dt != sale_date
            ]
            if not related_buys:
                continue
            disallowed = round(abs(loss), 2)
            flagged.append(
                {
                    "asset": asset,
                    "sell_transaction": tx,
                    "matching_buy_dates": related_buys,
                    "disallowed_loss": disallowed,
                    "adjusted_cost_basis": round(cost_basis + disallowed, 2),
                }
            )

        data = {"flagged_sales": flagged}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("wash_sale_detector", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _normalize_tx(tx: dict[str, Any]) -> dict[str, Any]:
    try:
        tx_date = datetime.fromisoformat(str(tx.get("date"))).replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise ValueError(f"Invalid date: {tx.get('date')}") from exc
    action = str(tx.get("action", "")).lower()
    if action not in {"buy", "sell"}:
        raise ValueError("action must be buy or sell")
    return {
        "asset": str(tx.get("asset", "")).upper(),
        "action": action,
        "date": tx_date,
        "amount": float(tx.get("amount", 0.0)),
        "price": float(tx.get("price", 0.0)),
    }


def _loss_from_sale(lots: list[dict[str, float]], sale: dict[str, Any]) -> tuple[float, float]:
    quantity_to_sell = sale["amount"]
    proceeds = quantity_to_sell * sale["price"]
    cost_basis = 0.0
    remaining_qty = quantity_to_sell
    for lot in lots:
        if remaining_qty <= 0:
            break
        take = min(remaining_qty, lot["quantity"])
        cost_basis += take * lot["price"]
        lot["quantity"] -= take
        remaining_qty -= take
    # remove depleted lots
    lots[:] = [lot for lot in lots if lot["quantity"] > 1e-9]
    if remaining_qty > 1e-9:
        # Assume unknown cost for uncovered quantity equals sale price
        cost_basis += remaining_qty * sale["price"]
    gain_loss = proceeds - cost_basis
    return gain_loss, cost_basis


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
