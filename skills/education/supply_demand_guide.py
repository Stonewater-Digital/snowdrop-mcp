"""Educational guide to supply and demand economics.

MCP Tool Name: supply_demand_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "supply_demand_guide",
    "description": "Returns educational content on supply and demand: law of supply/demand, equilibrium, elasticity, and shifts.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def supply_demand_guide() -> dict[str, Any]:
    """Returns educational content on supply and demand."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "Supply and demand is the fundamental economic model describing how prices are determined in a market. The interaction between buyers (demand) and sellers (supply) establishes the equilibrium price and quantity for goods and services.",
                "key_concepts": [
                    "The law of demand: as price rises, quantity demanded falls (and vice versa)",
                    "The law of supply: as price rises, quantity supplied rises (and vice versa)",
                    "Equilibrium occurs where the supply and demand curves intersect",
                    "Market forces naturally push prices toward equilibrium",
                ],
                "law_of_demand": {
                    "definition": "All else being equal, as the price of a good increases, the quantity demanded decreases, and as the price decreases, the quantity demanded increases.",
                    "demand_curve": "Slopes downward from left to right. Shows the inverse relationship between price and quantity demanded.",
                    "demand_shifters": [
                        "Income (normal goods: demand rises with income; inferior goods: demand falls with income)",
                        "Prices of related goods (substitutes and complements)",
                        "Consumer tastes and preferences",
                        "Population and demographics",
                        "Expectations about future prices",
                    ],
                },
                "law_of_supply": {
                    "definition": "All else being equal, as the price of a good increases, the quantity supplied increases, and as the price decreases, the quantity supplied decreases.",
                    "supply_curve": "Slopes upward from left to right. Shows the positive relationship between price and quantity supplied.",
                    "supply_shifters": [
                        "Input costs (raw materials, labor, energy)",
                        "Technology improvements (increase supply)",
                        "Number of sellers in the market",
                        "Government policies (taxes, subsidies, regulations)",
                        "Expectations about future prices",
                    ],
                },
                "equilibrium": {
                    "definition": "The price and quantity where quantity demanded equals quantity supplied. No surplus or shortage exists.",
                    "surplus": "When price is above equilibrium, quantity supplied exceeds quantity demanded. Sellers reduce prices to clear inventory.",
                    "shortage": "When price is below equilibrium, quantity demanded exceeds quantity supplied. Buyers bid prices up.",
                    "price_mechanism": "The market's self-correcting process that moves prices toward equilibrium through the forces of surplus and shortage.",
                },
                "elasticity": {
                    "price_elasticity_of_demand": "Measures how responsive quantity demanded is to a price change. Formula: % change in quantity demanded / % change in price.",
                    "elastic": "Elasticity > 1. Demand is very responsive to price changes. Examples: luxury goods, goods with close substitutes.",
                    "inelastic": "Elasticity < 1. Demand is relatively unresponsive to price changes. Examples: necessities (gasoline, medicine, food).",
                    "unit_elastic": "Elasticity = 1. Percentage change in quantity equals percentage change in price.",
                    "factors_affecting_elasticity": [
                        "Availability of substitutes (more substitutes = more elastic)",
                        "Necessity vs luxury (necessities are more inelastic)",
                        "Time horizon (demand becomes more elastic over time)",
                        "Proportion of income spent (higher proportion = more elastic)",
                    ],
                },
                "example": "In the housing market: if mortgage rates drop (cost of buying decreases), demand for houses shifts right (increases). If construction costs rise (input costs), supply shifts left (decreases). Both shifts push home prices higher. The magnitude depends on the elasticities of supply and demand.",
                "common_mistakes": [
                    "Confusing a shift of the curve (change in demand/supply) with a movement along the curve (change in quantity demanded/supplied)",
                    "Assuming all markets reach equilibrium quickly — some markets have significant frictions",
                    "Ignoring that supply and demand can shift simultaneously",
                    "Applying simple supply/demand models to markets with significant government intervention or monopoly power",
                    "Forgetting that ceteris paribus (all else equal) is an assumption that rarely holds in reality",
                ],
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
