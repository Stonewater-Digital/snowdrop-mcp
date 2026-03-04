"""Calculate refinery crack spreads."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "energy_crack_spread_calculator",
    "description": (
        "Computes 3-2-1 crack spread (standard refinery margin), custom ratio crack spread, "
        "1-1-1 simplified spread, and a margin compression flag. All prices in $/bbl."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "crude_price_per_bbl": {
                "type": "number",
                "description": "Crude oil input price per barrel (must be > 0).",
            },
            "gasoline_price_per_bbl": {
                "type": "number",
                "description": "Gasoline (RBOB) price per barrel (must be > 0).",
            },
            "distillate_price_per_bbl": {
                "type": "number",
                "description": "Distillate / heating oil / diesel price per barrel (must be > 0).",
            },
            "gasoline_ratio": {
                "type": "number",
                "default": 2,
                "description": "Barrels of gasoline produced per N barrels of crude (default 2 in 3-2-1).",
            },
            "distillate_ratio": {
                "type": "number",
                "default": 1,
                "description": "Barrels of distillate produced per N barrels of crude (default 1 in 3-2-1).",
            },
        },
        "required": [
            "crude_price_per_bbl",
            "gasoline_price_per_bbl",
            "distillate_price_per_bbl",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "three_two_one_crack_spread": {"type": "number"},
            "custom_crack_spread": {"type": "number"},
            "one_one_one_crack_spread": {"type": "number"},
            "margin_flag": {"type": "string"},
            "timestamp": {"type": "string"},
        },
    },
}


def energy_crack_spread_calculator(
    crude_price_per_bbl: float,
    gasoline_price_per_bbl: float,
    distillate_price_per_bbl: float,
    gasoline_ratio: float = 2,
    distillate_ratio: float = 1,
    **_: Any,
) -> dict[str, Any]:
    """Return crack spreads per barrel of crude processed.

    Args:
        crude_price_per_bbl: Crude oil input price per barrel.
        gasoline_price_per_bbl: Gasoline output price per barrel.
        distillate_price_per_bbl: Distillate output price per barrel.
        gasoline_ratio: Barrels of gasoline per batch (default 2).
        distillate_ratio: Barrels of distillate per batch (default 1).

    Returns:
        dict with status, three standard crack spread calculations, and margin_flag.

    Crack spread formulas (per barrel of crude input):

    3-2-1 crack spread (industry standard):
        (2 * gasoline + 1 * distillate) / 3 - crude
        Reflects a refinery that processes 3 bbl crude into 2 bbl gasoline + 1 bbl distillate.

    Custom ratio crack spread:
        (gas_ratio * gasoline + dist_ratio * distillate) / (gas_ratio + dist_ratio) - crude
        Weighted average product value minus crude cost.

    1-1-1 simplified spread:
        (gasoline + distillate) / 2 - crude
        Equal-weight blend of two products versus crude.
    """
    try:
        if crude_price_per_bbl <= 0:
            raise ValueError("crude_price_per_bbl must be positive")
        if gasoline_price_per_bbl <= 0:
            raise ValueError("gasoline_price_per_bbl must be positive")
        if distillate_price_per_bbl <= 0:
            raise ValueError("distillate_price_per_bbl must be positive")
        if gasoline_ratio < 0 or distillate_ratio < 0:
            raise ValueError("Product ratios must be non-negative")
        total_ratio = gasoline_ratio + distillate_ratio
        if total_ratio <= 0:
            raise ValueError("Sum of gasoline_ratio + distillate_ratio must be > 0")

        # Industry-standard 3-2-1: (2*gas + 1*dist)/3 - crude
        three_two_one = (
            (2.0 * gasoline_price_per_bbl + 1.0 * distillate_price_per_bbl) / 3.0
            - crude_price_per_bbl
        )

        # Custom ratio: weighted average product revenue minus crude
        custom = (
            (gasoline_ratio * gasoline_price_per_bbl + distillate_ratio * distillate_price_per_bbl)
            / total_ratio
            - crude_price_per_bbl
        )

        # 1-1-1 equal-weight spread
        one_one_one = (gasoline_price_per_bbl + distillate_price_per_bbl) / 2.0 - crude_price_per_bbl

        # Margin flag based on 3-2-1 (industry standard threshold ~$10/bbl)
        margin_flag = "compressed" if three_two_one < 10.0 else "healthy"

        return {
            "status": "success",
            "three_two_one_crack_spread": round(three_two_one, 2),
            "custom_crack_spread": round(custom, 2),
            "one_one_one_crack_spread": round(one_one_one, 2),
            "margin_flag": margin_flag,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("energy_crack_spread_calculator", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
