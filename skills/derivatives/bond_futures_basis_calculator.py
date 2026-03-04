"""Bond futures basis calculator."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "bond_futures_basis_calculator",
    "description": "Identifies CTD bond and computes gross/net basis for bond futures.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "bonds": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "cusip": {"type": "string"},
                        "price": {"type": "number", "description": "Full (dirty) price of the bond."},
                        "conversion_factor": {"type": "number", "description": "Futures conversion factor (CF)."},
                        "coupon_pct": {"type": "number", "description": "Annual coupon rate as a percentage."},
                    },
                    "required": ["price", "conversion_factor"],
                },
                "description": "List of deliverable bonds.",
            },
            "futures_price": {"type": "number", "description": "Current futures price (clean). Must be > 0."},
            "financing_rate_pct": {"type": "number", "description": "Repo / financing rate as a percentage (annual, actual/360)."},
            "days_to_delivery": {"type": "integer", "description": "Days from today to futures delivery date. Must be >= 1."},
        },
        "required": ["bonds", "futures_price", "financing_rate_pct", "days_to_delivery"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "ctd_bond": {"type": "object"},
                    "all_bonds": {"type": "array"},
                    "net_basis": {"type": "number"},
                    "delivery_option_value": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def bond_futures_basis_calculator(
    bonds: list[dict[str, Any]],
    futures_price: float,
    financing_rate_pct: float,
    days_to_delivery: int,
    **_: Any,
) -> dict[str, Any]:
    """Return CTD bond selection and basis metrics for bond futures.

    Definitions:
        invoice_price = futures_price * conversion_factor
        gross_basis   = bond_price - invoice_price
        carry         = (bond_price * repo_rate - coupon_rate * bond_price) * (days/360)
                      = bond_price * (repo_rate - coupon_rate) * (days/360)
        net_basis     = gross_basis - carry
        implied_repo  = (invoice_price - bond_price) / bond_price * (360 / days)
    CTD = bond with the lowest net basis (most attractive to deliver).

    Args:
        bonds: List of deliverable bonds with price, conversion_factor, coupon_pct.
        futures_price: Current futures clean price (must be > 0).
        financing_rate_pct: Repo rate as a percentage.
        days_to_delivery: Days to futures delivery (must be >= 1).

    Returns:
        dict with ctd_bond, all_bonds metrics, net_basis, delivery_option_value.
    """
    try:
        if not bonds:
            raise ValueError("bonds list must not be empty")
        if futures_price <= 0:
            raise ValueError("futures_price must be positive")
        if days_to_delivery < 1:
            raise ValueError("days_to_delivery must be at least 1")

        repo_rate = financing_rate_pct / 100.0
        year_fraction = days_to_delivery / 360.0

        best_net_basis = float("inf")
        ctd: dict[str, Any] | None = None
        all_results: list[dict[str, Any]] = []

        for bond in bonds:
            price = float(bond.get("price", 0.0))
            cf = float(bond.get("conversion_factor", 1.0))
            coupon_rate = float(bond.get("coupon_pct", 0.0)) / 100.0

            if price <= 0:
                raise ValueError(f"Bond price must be positive, got {price}")
            if cf <= 0:
                raise ValueError(f"conversion_factor must be positive, got {cf}")

            invoice_price = futures_price * cf
            gross_basis = price - invoice_price

            # Carry = financing cost of holding bond - coupon received
            # = price * repo_rate * T - coupon_rate * price * T
            # = price * (repo_rate - coupon_rate) * T
            carry = price * (repo_rate - coupon_rate) * year_fraction
            net_basis = gross_basis - carry

            # Implied repo: annualised return from buying bond and delivering into futures
            # = (invoice_price - price) / price * (360 / days)
            implied_repo_rate = (invoice_price - price) / price / year_fraction if price else 0.0

            record: dict[str, Any] = {
                "cusip": bond.get("cusip"),
                "price": round(price, 4),
                "conversion_factor": round(cf, 6),
                "invoice_price": round(invoice_price, 4),
                "gross_basis": round(gross_basis, 4),
                "carry": round(carry, 4),
                "net_basis": round(net_basis, 4),
                "implied_repo_rate_pct": round(implied_repo_rate * 100, 4),
            }
            all_results.append(record)

            if net_basis < best_net_basis:
                best_net_basis = net_basis
                ctd = record

        # Delivery option value: benefit to short from having choice of CTD
        delivery_option_value = abs(min(0.0, best_net_basis))

        data = {
            "ctd_bond": ctd,
            "all_bonds": all_results,
            "net_basis": round(best_net_basis, 4),
            "delivery_option_value": round(delivery_option_value, 4),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson(f"bond_futures_basis_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
