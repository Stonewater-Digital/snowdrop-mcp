"""
Executive Summary: Finds the cheapest and fastest cross-border remittance paths by computing total cost across provider corridors and filtering by urgency.
Inputs: transfer (dict: amount_usd, source_country, dest_country, urgency), corridors (list[dict]: provider, fee_pct, flat_fee, fx_markup_pct, speed_hours)
Outputs: ranked_options (list sorted by total_cost), cheapest (dict), fastest (dict), avg_cost_pct (float)
MCP Tool Name: remittance_cost_optimizer
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "remittance_cost_optimizer",
    "description": "Ranks cross-border remittance corridors by total cost, identifies cheapest and fastest options, and filters by urgency.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "transfer": {
                "type": "object",
                "description": "Transfer requirements",
                "properties": {
                    "amount_usd": {"type": "number", "description": "Transfer amount in USD"},
                    "source_country": {"type": "string", "description": "ISO 3166-1 alpha-2 source country"},
                    "dest_country": {"type": "string", "description": "ISO 3166-1 alpha-2 destination country"},
                    "urgency": {"type": "string", "enum": ["standard", "express"], "description": "standard = any speed, express = must arrive < 24h"}
                },
                "required": ["amount_usd", "source_country", "dest_country", "urgency"]
            },
            "corridors": {
                "type": "array",
                "description": "Available remittance providers/corridors",
                "items": {
                    "type": "object",
                    "properties": {
                        "provider": {"type": "string"},
                        "fee_pct": {"type": "number", "description": "Percentage fee (e.g. 1.5 for 1.5%)"},
                        "flat_fee": {"type": "number", "description": "Flat fee in USD"},
                        "fx_markup_pct": {"type": "number", "description": "FX spread markup percentage"},
                        "speed_hours": {"type": "number", "description": "Estimated delivery time in hours"}
                    },
                    "required": ["provider", "fee_pct", "flat_fee", "fx_markup_pct", "speed_hours"]
                }
            }
        },
        "required": ["transfer", "corridors"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "ranked_options": {"type": "array"},
                    "cheapest": {"type": "object"},
                    "fastest": {"type": "object"},
                    "avg_cost_pct": {"type": "number"}
                }
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "data", "timestamp"]
    }
}

# Express threshold in hours (World Bank definition: < 24h)
EXPRESS_THRESHOLD_HOURS = 24.0

# World Bank target: remittance cost <= 3% of transfer amount (SDG 10.c.1)
WORLD_BANK_TARGET_PCT = 3.0


def _compute_corridor_cost(
    amount_usd: float,
    fee_pct: float,
    flat_fee: float,
    fx_markup_pct: float,
) -> tuple[float, float]:
    """Compute total cost and effective cost percentage for a corridor.

    Total cost model:
      transaction_fee = amount * fee_pct/100 + flat_fee
      fx_cost = amount * fx_markup_pct/100
      total_cost = transaction_fee + fx_cost
      recipient_gets = amount - total_cost

    Args:
        amount_usd: Transfer amount in USD.
        fee_pct: Percentage-based transaction fee.
        flat_fee: Fixed USD fee regardless of amount.
        fx_markup_pct: FX spread markup as percentage.

    Returns:
        tuple[float, float]: (total_cost_usd, cost_pct_of_amount)
    """
    transaction_fee = amount_usd * fee_pct / 100.0 + flat_fee
    fx_cost = amount_usd * fx_markup_pct / 100.0
    total_cost = transaction_fee + fx_cost
    cost_pct = total_cost / amount_usd * 100.0
    return total_cost, cost_pct


def remittance_cost_optimizer(
    transfer: dict[str, Any],
    corridors: list[dict[str, Any]],
    **kwargs: Any
) -> dict[str, Any]:
    """Rank remittance corridors by total cost and identify optimal options.

    Computes all-in cost for each provider (transaction fee + flat fee +
    FX markup), ranks by ascending total cost, and separately identifies
    the fastest corridor. Flags World Bank SDG 10.c.1 compliance (<=3% cost).

    Args:
        transfer: Dictionary containing:
            - amount_usd (float): Transfer amount in USD.
            - source_country (str): Sender's country code.
            - dest_country (str): Recipient's country code.
            - urgency (str): 'standard' (any speed) or 'express' (<24h).
        corridors: List of provider dicts. Each must have:
            - provider (str): Provider name.
            - fee_pct (float): Percentage fee.
            - flat_fee (float): Flat USD fee.
            - fx_markup_pct (float): FX markup percentage.
            - speed_hours (float): Estimated delivery hours.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Standard Snowdrop response envelope with keys:
            - status (str): 'success' or 'error'.
            - data (dict): Results including ranked_options (list sorted by
              total_cost), cheapest (dict), fastest (dict), avg_cost_pct (float),
              world_bank_compliant_count (int), express_options (list),
              savings_vs_worst (dict), and transfer_summary.
            - timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        amount_usd = float(transfer.get("amount_usd", 0.0))
        source_country = str(transfer.get("source_country", "")).upper().strip()
        dest_country = str(transfer.get("dest_country", "")).upper().strip()
        urgency = str(transfer.get("urgency", "standard")).lower().strip()

        if amount_usd <= 0:
            raise ValueError("amount_usd must be positive")
        if not corridors:
            raise ValueError("corridors must be non-empty")
        if urgency not in ("standard", "express"):
            raise ValueError("urgency must be 'standard' or 'express'")

        # Compute costs for all corridors
        computed_corridors: list[dict[str, Any]] = []

        for corridor in corridors:
            provider = str(corridor.get("provider", "UNKNOWN")).strip()
            fee_pct = float(corridor.get("fee_pct", 0.0))
            flat_fee = float(corridor.get("flat_fee", 0.0))
            fx_markup_pct = float(corridor.get("fx_markup_pct", 0.0))
            speed_hours = float(corridor.get("speed_hours", 0.0))

            total_cost, cost_pct = _compute_corridor_cost(amount_usd, fee_pct, flat_fee, fx_markup_pct)
            recipient_gets = round(amount_usd - total_cost, 2)
            is_express = speed_hours < EXPRESS_THRESHOLD_HOURS
            world_bank_compliant = cost_pct <= WORLD_BANK_TARGET_PCT

            computed_corridors.append({
                "provider": provider,
                "fee_pct": fee_pct,
                "flat_fee_usd": flat_fee,
                "fx_markup_pct": fx_markup_pct,
                "transaction_fee_usd": round(amount_usd * fee_pct / 100.0 + flat_fee, 4),
                "fx_cost_usd": round(amount_usd * fx_markup_pct / 100.0, 4),
                "total_cost_usd": round(total_cost, 4),
                "total_cost_pct": round(cost_pct, 4),
                "recipient_gets_usd": recipient_gets,
                "speed_hours": speed_hours,
                "is_express": is_express,
                "world_bank_compliant": world_bank_compliant,
            })

        # Sort by total cost ascending
        ranked_options: list[dict[str, Any]] = sorted(
            computed_corridors, key=lambda x: x["total_cost_usd"]
        )

        # Add rank
        for i, opt in enumerate(ranked_options, 1):
            opt["rank"] = i

        # Filter for urgency
        express_options: list[dict[str, Any]] = [
            c for c in ranked_options if c["is_express"]
        ]

        # Apply urgency filter for ranking if express
        eligible_options = express_options if urgency == "express" else ranked_options
        if urgency == "express" and not eligible_options:
            return {
                "status": "error",
                "error": f"No express (<{EXPRESS_THRESHOLD_HOURS}h) corridors available for this transfer",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        cheapest: dict[str, Any] = eligible_options[0] if eligible_options else {}
        fastest: dict[str, Any] = min(computed_corridors, key=lambda x: x["speed_hours"]) if computed_corridors else {}
        worst_cost = ranked_options[-1]["total_cost_usd"] if ranked_options else 0.0

        avg_cost_pct: float = round(
            sum(c["total_cost_pct"] for c in computed_corridors) / len(computed_corridors), 4
        )

        savings_vs_worst: dict[str, Any] = {}
        if cheapest and ranked_options:
            savings_usd = round(worst_cost - cheapest["total_cost_usd"], 4)
            savings_pct = round(savings_usd / amount_usd * 100, 4)
            savings_vs_worst = {
                "cheapest_provider": cheapest["provider"],
                "worst_provider": ranked_options[-1]["provider"],
                "savings_usd": savings_usd,
                "savings_pct": savings_pct,
                "worst_cost_usd": worst_cost,
                "cheapest_cost_usd": cheapest["total_cost_usd"],
            }

        world_bank_compliant_count = sum(1 for c in computed_corridors if c["world_bank_compliant"])

        result: dict[str, Any] = {
            "ranked_options": ranked_options,
            "cheapest": cheapest,
            "fastest": fastest,
            "avg_cost_pct": avg_cost_pct,
            "express_options": express_options,
            "express_options_count": len(express_options),
            "world_bank_compliant_count": world_bank_compliant_count,
            "world_bank_target_pct": WORLD_BANK_TARGET_PCT,
            "savings_vs_worst": savings_vs_worst,
            "transfer_summary": {
                "amount_usd": amount_usd,
                "source_country": source_country,
                "dest_country": dest_country,
                "urgency": urgency,
                "corridors_evaluated": len(corridors),
            },
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"remittance_cost_optimizer failed: {e}")
        _log_lesson(f"remittance_cost_optimizer: {e}")
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
