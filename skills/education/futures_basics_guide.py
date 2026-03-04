"""Educational guide to futures contracts and trading fundamentals.

MCP Tool Name: futures_basics_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "futures_basics_guide",
    "description": "Returns educational content on futures: definition, margin, mark-to-market, hedging vs speculation.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def futures_basics_guide() -> dict[str, Any]:
    """Returns educational content on futures contracts."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "A futures contract is a standardized legal agreement to buy or sell a specific quantity of an asset at a predetermined price on a specified future date. Unlike options, both the buyer and seller are obligated to fulfill the contract. Futures trade on regulated exchanges (CME, CBOT, NYMEX).",
                "key_concepts": [
                    "Futures are zero-sum — every dollar gained by one party is lost by another",
                    "Most futures contracts are closed out before delivery (cash-settled or offset)",
                    "Leverage through margin means small price moves create large percentage gains or losses",
                    "Futures prices converge with spot prices as expiration approaches (basis convergence)",
                ],
                "formula": "Futures Price (theoretical) = Spot Price * (1 + r - d)^t, where r = risk-free rate, d = dividend/storage cost yield, t = time to expiration",
                "margin_system": {
                    "initial_margin": "The deposit required to open a futures position, typically 5-15% of the contract's full value. Set by the exchange.",
                    "maintenance_margin": "The minimum account balance that must be maintained. Usually 75% of initial margin.",
                    "margin_call": "If the account falls below maintenance margin, the trader must deposit additional funds (variation margin) to restore the initial margin level. Failure to meet a margin call results in forced liquidation.",
                },
                "mark_to_market": {
                    "definition": "The daily settlement process where gains and losses are calculated based on the day's closing price and credited/debited to each party's margin account.",
                    "how_it_works": "At the end of each trading day, the exchange clearinghouse calculates the difference between today's settlement price and yesterday's. Winners are credited, losers are debited.",
                    "purpose": "Eliminates the accumulation of large unpaid obligations. Ensures counterparty risk is managed on a daily basis.",
                },
                "hedging_vs_speculation": {
                    "hedging": {
                        "definition": "Using futures to lock in prices and reduce risk exposure in the physical market.",
                        "example": "A wheat farmer sells wheat futures to lock in a price for their harvest. If wheat prices fall, the futures gain offsets the lower cash price received.",
                        "who_hedges": "Farmers, airlines (fuel), manufacturers (raw materials), importers/exporters (currency).",
                    },
                    "speculation": {
                        "definition": "Taking futures positions to profit from expected price movements without an underlying physical exposure.",
                        "example": "A trader buys crude oil futures expecting prices to rise. If oil rises $2/barrel, profit = $2 * 1,000 barrels = $2,000 per contract.",
                        "role_in_markets": "Speculators provide liquidity and help with price discovery, making hedging more efficient.",
                    },
                },
                "common_futures_markets": {
                    "commodities": "Crude oil, natural gas, gold, silver, corn, wheat, soybeans, cattle",
                    "financials": "S&P 500 (ES), Nasdaq (NQ), Treasury bonds, Eurodollars",
                    "currencies": "EUR/USD, JPY/USD, GBP/USD, AUD/USD",
                },
                "example": "An airline buys 100 crude oil futures contracts at $75/barrel to hedge fuel costs. Each contract = 1,000 barrels. If oil rises to $85, the $10/barrel gain on futures ($1,000,000 total) offsets the higher fuel purchase cost.",
                "common_mistakes": [
                    "Underestimating leverage — a 5% margin means a 10% price move creates a 200% gain or loss on capital",
                    "Failing to maintain adequate margin and getting forcibly liquidated at the worst time",
                    "Not understanding contract specifications (expiration, settlement, delivery terms)",
                    "Rolling contracts too late and incurring losses from contango or backwardation",
                    "Using futures for speculation without a clear risk management plan and stop-loss discipline",
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
