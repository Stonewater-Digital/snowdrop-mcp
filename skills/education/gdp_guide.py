"""Educational guide to Gross Domestic Product (GDP).

MCP Tool Name: gdp_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "gdp_guide",
    "description": "Returns educational content on GDP: definition, components (C+I+G+NX), nominal vs real, and growth rate.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def gdp_guide() -> dict[str, Any]:
    """Returns educational content on Gross Domestic Product."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "Gross Domestic Product (GDP) is the total monetary value of all final goods and services produced within a country's borders during a specific time period (usually a quarter or a year). It is the most comprehensive measure of a nation's economic output and health.",
                "key_concepts": [
                    "GDP measures production within borders, regardless of who produces it",
                    "Only final goods are counted — intermediate goods are excluded to avoid double-counting",
                    "GDP can be measured by expenditure, income, or production approaches",
                    "Two consecutive quarters of negative GDP growth is often called a recession",
                ],
                "formula": "GDP = C + I + G + (X - M), where C = Consumer spending, I = Business investment, G = Government spending, X = Exports, M = Imports",
                "components": {
                    "consumption_C": {
                        "share": "~68% of U.S. GDP",
                        "description": "Household spending on goods and services: durable goods (cars, appliances), nondurable goods (food, clothing), and services (healthcare, housing, entertainment).",
                    },
                    "investment_I": {
                        "share": "~18% of U.S. GDP",
                        "description": "Business spending on capital equipment, structures, and inventory changes. Also includes residential construction. Does NOT include financial investments (stocks, bonds).",
                    },
                    "government_G": {
                        "share": "~17% of U.S. GDP",
                        "description": "Federal, state, and local government spending on goods and services (defense, infrastructure, education). Excludes transfer payments (Social Security, welfare) as those are not purchases of new goods/services.",
                    },
                    "net_exports_NX": {
                        "share": "~-3% of U.S. GDP (trade deficit)",
                        "description": "Exports minus imports. A trade surplus (X > M) adds to GDP; a trade deficit (M > X) subtracts from GDP. The U.S. has run trade deficits since the 1970s.",
                    },
                },
                "nominal_vs_real": {
                    "nominal_gdp": "Measured at current market prices. Includes the effects of both production changes and price changes (inflation). Useful for comparing economies at a point in time.",
                    "real_gdp": "Adjusted for inflation using a base year's prices (GDP deflator). Isolates the change in actual output. Used for comparing growth over time.",
                    "gdp_deflator": "GDP Deflator = (Nominal GDP / Real GDP) * 100. A broader measure of price changes than CPI because it covers all goods and services produced, not just a consumer basket.",
                },
                "growth_rate": {
                    "formula": "GDP Growth Rate = ((GDP_current - GDP_previous) / GDP_previous) * 100",
                    "annualized": "Quarterly GDP growth is typically reported as an annualized rate: (1 + quarterly rate)^4 - 1.",
                    "healthy_growth": "2-3% real GDP growth is considered healthy for developed economies like the U.S.",
                    "recession": "Commonly defined as two consecutive quarters of negative real GDP growth, though the NBER uses broader criteria.",
                    "per_capita": "GDP per capita = GDP / Population. Better measure of individual living standards than total GDP.",
                },
                "example": "If a country has consumer spending of $14T, business investment of $3.5T, government spending of $3.5T, exports of $2.5T, and imports of $3.5T: GDP = $14T + $3.5T + $3.5T + ($2.5T - $3.5T) = $20T.",
                "common_mistakes": [
                    "Confusing GDP with GNP (Gross National Product, which measures output by a country's citizens regardless of location)",
                    "Assuming GDP measures well-being — it excludes unpaid work, leisure, environmental quality, and income distribution",
                    "Comparing nominal GDP across years without adjusting for inflation",
                    "Ignoring the difference between GDP level and GDP growth rate",
                    "Using GDP alone to compare living standards without adjusting for purchasing power parity (PPP)",
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
