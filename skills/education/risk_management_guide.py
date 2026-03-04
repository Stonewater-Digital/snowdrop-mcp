"""Educational guide to financial risk management fundamentals.

MCP Tool Name: risk_management_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "risk_management_guide",
    "description": "Returns educational content on types of financial risk, mitigation strategies, and hedging basics.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def risk_management_guide() -> dict[str, Any]:
    """Returns educational content on financial risk management."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "Risk management is the process of identifying, assessing, and controlling threats to an organization's capital and earnings, or an investor's portfolio value. It involves understanding the types of risk, measuring exposure, and implementing strategies to mitigate potential losses.",
                "key_concepts": [
                    "Risk and return are positively correlated — higher potential returns generally require accepting more risk",
                    "Diversification is the only free lunch in finance",
                    "Risk cannot be eliminated, only managed and transferred",
                    "The goal is risk-adjusted returns, not return maximization",
                ],
                "types_of_risk": {
                    "market_risk": "Risk of losses due to movements in market prices (stock prices, interest rates, exchange rates). Also called systematic risk — cannot be diversified away.",
                    "credit_risk": "Risk that a borrower or counterparty will fail to meet their obligations. Measured by credit ratings and credit default swap spreads.",
                    "liquidity_risk": "Risk of being unable to sell an asset quickly enough at a fair price. More pronounced in small-cap stocks, real estate, and exotic derivatives.",
                    "operational_risk": "Risk of loss from inadequate internal processes, people, systems, or external events. Includes fraud, technology failures, and natural disasters.",
                    "inflation_risk": "Risk that inflation erodes the purchasing power of investment returns. Particularly relevant for fixed-income investors.",
                    "interest_rate_risk": "Risk that changes in interest rates will affect the value of investments, especially bonds. Duration measures this sensitivity.",
                    "currency_risk": "Risk from changes in exchange rates affecting international investments. Can be hedged with currency forwards or options.",
                    "concentration_risk": "Risk from having too large a position in a single asset, sector, or geographic region.",
                    "regulatory_risk": "Risk from changes in laws, regulations, or tax policies that affect investment values or business operations.",
                },
                "mitigation_strategies": {
                    "diversification": "Spread investments across asset classes, sectors, geographies, and time horizons to reduce unsystematic risk.",
                    "asset_allocation": "Determine the optimal mix of stocks, bonds, cash, and alternatives based on risk tolerance, time horizon, and goals.",
                    "position_sizing": "Limit any single position to a small percentage of the portfolio (commonly 1-5%) to cap potential losses.",
                    "stop_loss_orders": "Automatic sell orders triggered at predetermined price levels to limit downside exposure.",
                    "rebalancing": "Periodically adjust portfolio weights back to target allocations, selling winners and buying laggards.",
                    "insurance": "Transfer specific risks to an insurance company (property, liability, life, disability).",
                    "due_diligence": "Thorough research and analysis before making investment decisions to understand risks upfront.",
                },
                "hedging_basics": {
                    "definition": "Hedging is taking an offsetting position to reduce or eliminate specific risk exposure. Like buying insurance for your portfolio.",
                    "common_instruments": {
                        "put_options": "Buy put options to protect against stock price declines. Cost is the premium paid.",
                        "futures_contracts": "Lock in prices for commodities or currencies. Used by producers and consumers to manage price risk.",
                        "inverse_etfs": "ETFs that move opposite to their benchmark index. Simple way to hedge market exposure.",
                        "currency_forwards": "Agreements to exchange currencies at a future date at a predetermined rate.",
                    },
                    "cost_of_hedging": "Hedging reduces risk but also limits upside potential. The cost of protection (premiums, spreads) must be weighed against the risk being mitigated.",
                },
                "common_mistakes": [
                    "Confusing risk tolerance with risk capacity (willingness vs ability to take risk)",
                    "Over-concentrating in familiar assets (home bias, employer stock)",
                    "Ignoring tail risks — low-probability, high-impact events",
                    "Hedging too much, creating excessive drag on returns",
                    "Using leverage without understanding the amplified downside",
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
