"""Educational guide to foreign exchange (forex) trading fundamentals.

MCP Tool Name: forex_basics_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "forex_basics_guide",
    "description": "Returns educational content on forex: currency pairs, pips, lots, major/minor/exotic pairs.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def forex_basics_guide() -> dict[str, Any]:
    """Returns educational content on forex trading fundamentals."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "The foreign exchange (forex or FX) market is the largest and most liquid financial market in the world, with over $7 trillion in daily trading volume. It is a decentralized, over-the-counter (OTC) market where currencies are traded in pairs, 24 hours a day, five days a week.",
                "key_concepts": [
                    "Currencies are always traded in pairs — buying one means selling another",
                    "The forex market operates 24/5 across major sessions: Sydney, Tokyo, London, New York",
                    "High leverage is common (50:1 to 500:1 depending on jurisdiction), amplifying both gains and losses",
                    "Exchange rates are driven by interest rate differentials, economic data, geopolitics, and market sentiment",
                ],
                "currency_pairs": {
                    "base_and_quote": "In EUR/USD = 1.1050, EUR is the base currency and USD is the quote currency. It means 1 EUR costs 1.1050 USD.",
                    "major_pairs": [
                        "EUR/USD (Euro/US Dollar) — most traded pair globally",
                        "USD/JPY (US Dollar/Japanese Yen)",
                        "GBP/USD (British Pound/US Dollar)",
                        "USD/CHF (US Dollar/Swiss Franc)",
                        "AUD/USD (Australian Dollar/US Dollar)",
                        "USD/CAD (US Dollar/Canadian Dollar)",
                        "NZD/USD (New Zealand Dollar/US Dollar)",
                    ],
                    "minor_pairs": "Cross-currency pairs that do not include the US Dollar: EUR/GBP, EUR/JPY, GBP/JPY, AUD/NZD.",
                    "exotic_pairs": "Pairs involving a major currency and a developing economy currency: USD/TRY, USD/ZAR, EUR/PLN. Wider spreads and lower liquidity.",
                },
                "pips": {
                    "definition": "A pip (Percentage in Point) is the smallest standard price movement in a currency pair. For most pairs, 1 pip = 0.0001 (the fourth decimal place).",
                    "exception": "For JPY pairs, 1 pip = 0.01 (the second decimal place).",
                    "pip_value": "For a standard lot (100,000 units), 1 pip of EUR/USD = $10. For a mini lot (10,000 units), 1 pip = $1. For a micro lot (1,000 units), 1 pip = $0.10.",
                    "pipette": "A fractional pip, or 1/10 of a pip (the fifth decimal place for most pairs). Used by brokers for tighter pricing.",
                },
                "lot_sizes": {
                    "standard_lot": "100,000 units of the base currency. 1 pip = ~$10 for USD-quoted pairs.",
                    "mini_lot": "10,000 units of the base currency. 1 pip = ~$1.",
                    "micro_lot": "1,000 units of the base currency. 1 pip = ~$0.10.",
                    "nano_lot": "100 units of the base currency. 1 pip = ~$0.01. Available at some brokers.",
                },
                "key_terms": {
                    "spread": "The difference between the bid (sell) and ask (buy) price. This is the primary transaction cost in forex. Major pairs have tighter spreads (0.5-2 pips).",
                    "leverage": "Allows controlling a large position with a small deposit. 100:1 leverage means $1,000 controls $100,000. Amplifies both profits and losses.",
                    "margin": "The deposit required to maintain a leveraged position. At 100:1, a $100,000 position requires $1,000 margin.",
                    "swap_rate": "The interest rate differential paid or received for holding a position overnight. Based on the interest rate difference between the two currencies.",
                },
                "example": "Buying 1 standard lot of EUR/USD at 1.1050 with 50:1 leverage requires $2,210 margin ($110,500 / 50). If EUR/USD rises to 1.1100 (50 pips), profit = 50 pips * $10 = $500. If it falls to 1.1000 (50 pips), loss = $500.",
                "common_mistakes": [
                    "Using excessive leverage without understanding the risk of rapid account depletion",
                    "Trading exotic pairs without accounting for wide spreads and low liquidity",
                    "Ignoring the impact of swap/rollover costs on longer-term positions",
                    "Over-trading based on short-term noise rather than established trends or fundamentals",
                    "Not using stop-loss orders to manage risk in a 24-hour market",
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
