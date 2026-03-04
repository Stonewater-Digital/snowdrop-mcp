"""Simple trading strategy backtester for Snowdrop analytics."""
from __future__ import annotations

import math
import statistics
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "strategy_backtester",
    "description": "Runs deterministic backtests for rule-based trading strategies.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "strategy": {"type": "object"},
            "price_history": {
                "type": "array",
                "items": {"type": "object"},
            },
            "initial_capital": {
                "type": "number",
                "description": "Starting cash for the simulation.",
            },
        },
        "required": ["strategy", "price_history", "initial_capital"],
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


def strategy_backtester(
    strategy: dict[str, Any],
    price_history: list[dict[str, Any]],
    initial_capital: float,
    **_: Any,
) -> dict[str, Any]:
    """Backtest a rule-based long-only strategy."""
    try:
        if initial_capital <= 0:
            raise ValueError("initial_capital must be positive")
        if not isinstance(strategy, dict):
            raise ValueError("strategy must be a dict")
        if not isinstance(price_history, list) or not price_history:
            raise ValueError("price_history must be a non-empty list")

        entry_rules = strategy.get("entry_rules", []) or []
        exit_rules = strategy.get("exit_rules", []) or []
        position_size_pct = float(strategy.get("position_size_pct", 1.0))
        position_size_pct = min(max(position_size_pct, 0.0), 1.0)

        sorted_prices = sorted(
            price_history,
            key=lambda bar: bar.get("date", ""),
        )

        cash = initial_capital
        position = 0.0
        entry_price = 0.0
        entry_date: str | None = None
        trade_log: list[dict[str, Any]] = []
        equity_curve: list[float] = [initial_capital]
        last_close_price: float | None = None
        last_date: str | None = None

        for bar in sorted_prices:
            close_price = _get_numeric(bar, "close")
            if close_price <= 0:
                continue
            date = str(bar.get("date", ""))
            last_close_price = close_price
            last_date = date

            if position == 0 and _rules_met(entry_rules, bar):
                allocation = cash * position_size_pct
                if allocation > 0:
                    position = allocation / close_price
                    cash -= allocation
                    entry_price = close_price
                    entry_date = date
            elif position > 0 and _rules_met(exit_rules, bar):
                cash, position, trade, entry_price, entry_date = _close_position(
                    cash, position, close_price, entry_price, entry_date, date
                )
                trade_log.append(trade)

            equity_curve.append(cash + position * close_price)

        if position > 0:
            if last_close_price is None:
                raise ValueError("Unable to settle open position; no valid closing price")
            cash, position, trade, entry_price, entry_date = _close_position(
                cash, position, last_close_price, entry_price, entry_date, last_date
            )
            trade_log.append(trade)
            equity_curve.append(cash)

        final_equity = cash
        total_return = (final_equity - initial_capital) / initial_capital
        max_drawdown = _max_drawdown(equity_curve)
        win_rate = _win_rate(trade_log)
        profit_factor = _profit_factor(trade_log)
        sharpe_ratio = _sharpe_ratio(equity_curve)

        result = {
            "trade_log": trade_log,
            "total_return": round(total_return, 4),
            "max_drawdown": round(max_drawdown, 4),
            "win_rate": round(win_rate, 4),
            "profit_factor": round(profit_factor, 4) if profit_factor is not None else None,
            "sharpe_ratio": round(sharpe_ratio, 4) if sharpe_ratio is not None else None,
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("strategy_backtester", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _rules_met(rules: list[dict[str, Any]], bar: dict[str, Any]) -> bool:
    if not rules:
        return False
    for rule in rules:
        field = rule.get("field", "close")
        operator = rule.get("operator", "gt")
        left = _get_numeric(bar, field)
        if "value" in rule:
            right = float(rule["value"])
        else:
            compare_field = rule.get("compare_to", "close")
            right = _get_numeric(bar, compare_field)
        if not _compare(operator, left, right):
            return False
    return True


def _compare(operator: str, left: float, right: float) -> bool:
    operator = operator.lower()
    if operator in {"gt", ">"}:
        return left > right
    if operator in {"gte", ">=", "ge"}:
        return left >= right
    if operator in {"lt", "<"}:
        return left < right
    if operator in {"lte", "<=", "le"}:
        return left <= right
    if operator == "eq":
        return math.isclose(left, right)
    raise ValueError(f"Unsupported operator: {operator}")


def _close_position(
    cash: float,
    position: float,
    close_price: float,
    entry_price: float,
    entry_date: str | None,
    exit_date: str | None,
) -> tuple[float, float, dict[str, Any], float, str | None]:
    proceeds = position * close_price
    cash += proceeds
    pnl = proceeds - (position * entry_price)
    return_pct = pnl / (position * entry_price) if entry_price > 0 else 0.0
    trade = {
        "entry_date": entry_date,
        "exit_date": exit_date,
        "entry_price": round(entry_price, 4),
        "exit_price": round(close_price, 4),
        "pnl": round(pnl, 2),
        "return_pct": round(return_pct, 4),
    }
    return cash, 0.0, trade, 0.0, None


def _get_numeric(bar: dict[str, Any], field: str) -> float:
    value = bar.get(field)
    if value is None:
        raise ValueError(f"Missing field {field} in price history entry")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:  # noqa: B904
        raise ValueError(f"Field {field} must be numeric") from exc


def _max_drawdown(equity_curve: list[float]) -> float:
    peak = equity_curve[0]
    max_dd = 0.0
    for value in equity_curve:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak if peak > 0 else 0.0
        max_dd = max(max_dd, drawdown)
    return max_dd


def _win_rate(trades: list[dict[str, Any]]) -> float:
    if not trades:
        return 0.0
    winners = sum(1 for trade in trades if trade["pnl"] > 0)
    return winners / len(trades)


def _profit_factor(trades: list[dict[str, Any]]) -> float | None:
    gross_profit = sum(trade["pnl"] for trade in trades if trade["pnl"] > 0)
    gross_loss = sum(-trade["pnl"] for trade in trades if trade["pnl"] < 0)
    if gross_loss == 0:
        return None
    return gross_profit / gross_loss if gross_loss else None


def _sharpe_ratio(equity_curve: list[float]) -> float | None:
    if len(equity_curve) < 2:
        return None
    returns = []
    for prev, curr in zip(equity_curve[:-1], equity_curve[1:]):
        if prev <= 0:
            continue
        returns.append((curr - prev) / prev)
    if not returns:
        return None
    avg = sum(returns) / len(returns)
    std = statistics.pstdev(returns)
    if std == 0:
        return None
    return (avg / std) * math.sqrt(252)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
