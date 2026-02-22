"""Model capitalization tables with dilution across funding rounds."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "cap_table_manager",
    "description": "Computes fully diluted ownership after venture rounds including option pools and notes.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "rounds": {"type": "array", "items": {"type": "object"}},
            "founders": {"type": "array", "items": {"type": "object"}},
            "option_pool_pct": {"type": "number", "default": 10.0},
            "outstanding_safes": {"type": ["array", "null"], "default": None},
            "outstanding_convertibles": {"type": ["array", "null"], "default": None},
        },
        "required": ["rounds", "founders"],
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


def cap_table_manager(
    rounds: list[dict[str, Any]],
    founders: list[dict[str, Any]],
    option_pool_pct: float = 10.0,
    outstanding_safes: list[dict[str, Any]] | None = None,
    outstanding_convertibles: list[dict[str, Any]] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Generate a cap table summary with dilution per stakeholder."""
    try:
        if not rounds:
            raise ValueError("At least one round is required")
        founder_shares = sum(float(f.get("shares", 0)) for f in founders)
        if founder_shares <= 0:
            raise ValueError("Founders must have positive shares")
        holders: dict[str, float] = {
            f.get("name", "founder_anon"): float(f.get("shares", 0)) for f in founders
        }
        option_pool_shares = founder_shares * option_pool_pct / max(1 - option_pool_pct / 100, 0.01)
        holders["Option Pool"] = option_pool_shares
        total_shares = founder_shares + option_pool_shares

        post_money = rounds[-1].get("pre_money_valuation", 0)
        current_pps = None
        history: list[dict[str, Any]] = []
        for round_info in rounds:
            pre_money = float(round_info.get("pre_money_valuation", 0))
            investment = float(round_info.get("investment_amount", 0))
            investor = round_info.get("investor_name", round_info.get("round_name", "investor"))
            if pre_money <= 0 or investment <= 0:
                raise ValueError("Rounds must include positive valuations and investments")
            price_per_share = pre_money / total_shares
            new_shares = investment / price_per_share
            holders[investor] = holders.get(investor, 0) + new_shares
            total_shares += new_shares
            post_money = pre_money + investment
            current_pps = price_per_share
            history.append(
                {
                    "round": round_info.get("round_name"),
                    "price_per_share": round(price_per_share, 4),
                    "new_shares": int(new_shares),
                    "post_money": post_money,
                }
            )

        safe_shares = _convert_safes(outstanding_safes or [], total_shares, current_pps or 1.0, post_money)
        conv_shares = _convert_convertibles(outstanding_convertibles or [], current_pps or 1.0)
        if safe_shares:
            holders["SAFE"] = safe_shares
            total_shares += safe_shares
        if conv_shares:
            holders["Convertibles"] = conv_shares
            total_shares += conv_shares

        cap_table = []
        founder_total_pct = 0.0
        for holder, shares in holders.items():
            pct = shares / total_shares * 100
            if holder not in {"Option Pool", "SAFE", "Convertibles"} and holder not in [
                r.get("investor_name") for r in rounds
            ]:
                founder_total_pct += pct
            cap_table.append({"holder": holder, "shares": int(round(shares)), "ownership_pct": round(pct, 4)})
        data = {
            "cap_table": sorted(cap_table, key=lambda row: row["ownership_pct"], reverse=True),
            "fully_diluted_shares": int(round(total_shares)),
            "founder_dilution_total_pct": round(100 - founder_total_pct, 4),
            "current_pps": round(current_pps or 0, 4),
            "post_money_valuation": float(post_money),
            "round_history": history,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("cap_table_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _convert_safes(
    safes: Iterable[dict[str, Any]],
    total_shares: float,
    current_pps: float,
    post_money: float,
) -> float:
    shares = 0.0
    for safe in safes:
        amount = float(safe.get("amount", 0))
        cap = float(safe.get("valuation_cap", post_money))
        discount = float(safe.get("discount_pct", 20.0)) / 100
        cap_price = cap / total_shares if total_shares else current_pps
        discount_price = current_pps * (1 - discount)
        conversion_price = min(cap_price, discount_price)
        shares += amount / max(conversion_price, 1e-6)
    return shares


def _convert_convertibles(convertibles: Iterable[dict[str, Any]], current_pps: float) -> float:
    shares = 0.0
    for note in convertibles:
        amount = float(note.get("amount", 0))
        discount = float(note.get("discount_pct", 15.0)) / 100
        conversion_price = current_pps * (1 - discount)
        shares += amount / max(conversion_price, 1e-6)
    return shares


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
