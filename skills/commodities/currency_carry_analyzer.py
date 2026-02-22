"""Evaluate currency carry trades using interest differentials."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "currency_carry_analyzer",
    "description": "Calculates carry yields, CIP deviations, and risk flags for FX pairs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "pairs": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["pairs"],
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


def currency_carry_analyzer(pairs: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return carry stats and CIP checks for FX pairs."""
    try:
        if not pairs:
            raise ValueError("pairs required")
        results = []
        best_pair = None
        best_carry = -1
        total_carry = 0.0
        cip_violations = []
        for pair in pairs:
            base_rate = pair.get("base_interest_rate", 0)
            quote_rate = pair.get("quote_interest_rate", 0)
            spot = pair.get("spot_rate", 0)
            forward = pair.get("forward_rate")
            carry = base_rate - quote_rate
            total_carry += carry
            if carry > best_carry:
                best_carry = carry
                best_pair = f"{pair.get('base_currency')}/{pair.get('quote_currency')}"
            cip_forward = spot * (1 + quote_rate / 100) / max(1 + base_rate / 100, 1e-6)
            if forward is not None and abs(forward - cip_forward) > 0.01:
                cip_violations.append(pair.get("base_currency"))
            results.append(
                {
                    "pair": f"{pair.get('base_currency')}/{pair.get('quote_currency')}",
                    "carry_bps": round(carry * 100, 2),
                    "forward_parity": round(cip_forward, 4),
                    "forward_rate": forward,
                }
            )
        risk_warning = "CIP deviations observed" if cip_violations else "Standard carry risk"
        data = {
            "pairs": results,
            "best_carry_pair": best_pair,
            "total_carry_bps": round(total_carry * 100, 2),
            "cip_violations": cip_violations,
            "risk_warning": risk_warning,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("currency_carry_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
