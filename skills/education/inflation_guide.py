"""Educational guide to inflation and its effects on investments.

MCP Tool Name: inflation_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "inflation_guide",
    "description": "Returns educational content on inflation: definition, CPI, causes, effects on investments, and TIPS.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def inflation_guide() -> dict[str, Any]:
    """Returns educational content on inflation."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "Inflation is the sustained increase in the general price level of goods and services in an economy over time, resulting in a decrease in the purchasing power of money. It is typically measured as an annual percentage change.",
                "key_concepts": [
                    "Inflation erodes the real value of money — $100 today buys less in the future",
                    "Central banks target moderate inflation (~2%) as a sign of a healthy economy",
                    "Deflation (negative inflation) can be more dangerous than moderate inflation",
                    "Real return = Nominal return - Inflation rate (approximately)",
                ],
                "cpi": {
                    "definition": "The Consumer Price Index (CPI) is the most widely used measure of inflation, tracking the average change in prices paid by urban consumers for a basket of goods and services.",
                    "components": "Housing (33%), transportation (17%), food (14%), medical care (9%), education/communication (7%), recreation (6%), apparel (3%), other (11%).",
                    "core_cpi": "Excludes volatile food and energy prices to show underlying inflation trends. Often preferred by the Federal Reserve for policy decisions.",
                    "pce": "Personal Consumption Expenditures Price Index — the Fed's preferred inflation measure. Broader than CPI and adjusts for consumer substitution between goods.",
                },
                "causes": {
                    "demand_pull": "Too much money chasing too few goods. When aggregate demand exceeds aggregate supply, prices rise. Often occurs in strong economic expansions.",
                    "cost_push": "Rising production costs (wages, raw materials, energy) push prices higher as producers pass costs to consumers. Supply shocks (oil crises) are a classic cause.",
                    "monetary_inflation": "Excessive growth in the money supply relative to economic output. When central banks print too much money, each unit of currency becomes worth less.",
                    "built_in": "Wage-price spiral where workers demand higher wages due to rising prices, which increases production costs, leading to further price increases.",
                },
                "effects_on_investments": {
                    "cash_and_savings": "Most vulnerable. Cash loses purchasing power directly. Savings accounts earning below the inflation rate produce negative real returns.",
                    "bonds": "Fixed coupon payments become worth less in real terms. Bond prices fall when inflation expectations rise (interest rates increase). Long-duration bonds are most affected.",
                    "stocks": "Mixed. Companies with pricing power can pass costs to consumers, protecting profits. High-growth stocks are more sensitive because their value depends on distant future earnings.",
                    "real_estate": "Generally a good inflation hedge. Property values and rents tend to rise with inflation. Mortgage debt is eroded by inflation.",
                    "commodities": "Often rise with inflation since they are the raw materials whose prices are increasing. Gold is traditionally seen as an inflation hedge.",
                    "tips": "Treasury Inflation-Protected Securities. Principal adjusts with CPI, providing a guaranteed real return above inflation.",
                },
                "tips_details": {
                    "definition": "TIPS are U.S. Treasury securities whose principal value is adjusted based on changes in the CPI.",
                    "how_they_work": "If inflation is 3%, a $1,000 TIPS principal becomes $1,030. Coupon payments are based on the adjusted principal, so they also increase with inflation.",
                    "real_yield": "TIPS trade at a real yield (above inflation). If a TIPS yields 1.5%, the total return is approximately inflation + 1.5%.",
                    "breakeven_rate": "The difference between nominal Treasury yield and TIPS yield of the same maturity. Represents the market's inflation expectation.",
                },
                "example": "At 3% annual inflation, $100,000 in purchasing power today becomes equivalent to $74,409 in 10 years and $55,368 in 20 years. An investment earning 7% nominal return with 3% inflation earns approximately 4% real return.",
                "common_mistakes": [
                    "Ignoring inflation when evaluating investment returns (focusing on nominal instead of real returns)",
                    "Holding too much cash during inflationary periods, guaranteeing loss of purchasing power",
                    "Assuming inflation is constant — it varies significantly over time and can spike unexpectedly",
                    "Confusing price level increases with inflation rate changes",
                    "Panic-buying inflation hedges after inflation has already been priced into markets",
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
