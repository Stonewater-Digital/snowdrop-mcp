"""Look up definitions and related terms for common financial terminology.

MCP Tool Name: financial_term_glossary
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "financial_term_glossary",
    "description": "Look up definitions, categories, and related terms for 30+ common financial terms.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "term": {
                "type": "string",
                "description": "The financial term to look up.",
            },
        },
        "required": ["term"],
    },
}

_GLOSSARY: dict[str, dict[str, Any]] = {
    "asset": {
        "definition": "A resource with economic value owned or controlled by an individual or entity, expected to provide future benefit.",
        "category": "Accounting",
        "related_terms": ["liability", "equity", "balance sheet", "net worth"],
    },
    "liability": {
        "definition": "A financial obligation or debt owed by an individual or entity to another party.",
        "category": "Accounting",
        "related_terms": ["asset", "debt", "balance sheet", "accounts payable"],
    },
    "equity": {
        "definition": "The residual interest in the assets of an entity after deducting liabilities. Also refers to ownership shares in a company.",
        "category": "Accounting",
        "related_terms": ["asset", "liability", "shareholders equity", "book value"],
    },
    "revenue": {
        "definition": "The total income generated from the sale of goods or services related to a company's primary operations.",
        "category": "Accounting",
        "related_terms": ["income", "top line", "sales", "gross profit"],
    },
    "ebitda": {
        "definition": "Earnings Before Interest, Taxes, Depreciation, and Amortization. A measure of a company's operating performance.",
        "category": "Valuation",
        "related_terms": ["operating income", "net income", "free cash flow", "enterprise value"],
    },
    "dividend": {
        "definition": "A distribution of a portion of a company's earnings to its shareholders, usually in cash or additional shares.",
        "category": "Investing",
        "related_terms": ["yield", "payout ratio", "ex-dividend date", "DRIP"],
    },
    "bond": {
        "definition": "A fixed-income instrument representing a loan from an investor to a borrower, typically corporate or governmental.",
        "category": "Fixed Income",
        "related_terms": ["coupon", "yield", "maturity", "duration", "face value"],
    },
    "yield": {
        "definition": "The income return on an investment, expressed as a percentage of the investment's cost or current market value.",
        "category": "Fixed Income",
        "related_terms": ["coupon rate", "yield to maturity", "current yield", "dividend yield"],
    },
    "market_capitalization": {
        "definition": "The total market value of a company's outstanding shares, calculated as share price multiplied by total shares outstanding.",
        "category": "Valuation",
        "related_terms": ["enterprise value", "large cap", "mid cap", "small cap"],
    },
    "pe_ratio": {
        "definition": "Price-to-Earnings ratio. A valuation metric comparing a company's current share price to its earnings per share.",
        "category": "Valuation",
        "related_terms": ["earnings per share", "PEG ratio", "forward PE", "trailing PE"],
    },
    "eps": {
        "definition": "Earnings Per Share. The portion of a company's profit allocated to each outstanding share of common stock.",
        "category": "Valuation",
        "related_terms": ["pe_ratio", "net income", "diluted EPS", "basic EPS"],
    },
    "beta": {
        "definition": "A measure of a stock's volatility relative to the overall market. A beta of 1 means the stock moves with the market.",
        "category": "Risk",
        "related_terms": ["alpha", "volatility", "systematic risk", "CAPM"],
    },
    "alpha": {
        "definition": "The excess return of an investment relative to the return of a benchmark index. Positive alpha indicates outperformance.",
        "category": "Risk",
        "related_terms": ["beta", "benchmark", "active management", "Jensen's alpha"],
    },
    "volatility": {
        "definition": "A statistical measure of the dispersion of returns for a given security or market index, often measured by standard deviation.",
        "category": "Risk",
        "related_terms": ["beta", "standard deviation", "VIX", "implied volatility"],
    },
    "liquidity": {
        "definition": "The ease with which an asset can be converted into cash without significantly affecting its market price.",
        "category": "Markets",
        "related_terms": ["bid-ask spread", "volume", "market depth", "illiquidity premium"],
    },
    "leverage": {
        "definition": "The use of borrowed capital to increase the potential return of an investment. Also measured as the debt-to-equity ratio.",
        "category": "Corporate Finance",
        "related_terms": ["debt-to-equity", "margin", "financial leverage", "operating leverage"],
    },
    "amortization": {
        "definition": "The gradual reduction of a debt over time through regular payments, or the spreading of an intangible asset's cost over its useful life.",
        "category": "Accounting",
        "related_terms": ["depreciation", "principal", "loan schedule", "intangible asset"],
    },
    "depreciation": {
        "definition": "The systematic allocation of a tangible asset's cost over its useful life, representing wear and tear or obsolescence.",
        "category": "Accounting",
        "related_terms": ["amortization", "book value", "straight-line", "accelerated depreciation"],
    },
    "hedge": {
        "definition": "An investment made to reduce the risk of adverse price movements in an asset, typically using derivatives.",
        "category": "Risk Management",
        "related_terms": ["options", "futures", "derivatives", "risk mitigation"],
    },
    "derivative": {
        "definition": "A financial contract whose value is derived from the performance of an underlying asset, index, or rate.",
        "category": "Derivatives",
        "related_terms": ["options", "futures", "swaps", "forwards", "underlying asset"],
    },
    "option": {
        "definition": "A contract giving the buyer the right, but not the obligation, to buy (call) or sell (put) an asset at a specified price before a certain date.",
        "category": "Derivatives",
        "related_terms": ["call", "put", "strike price", "premium", "expiration"],
    },
    "futures": {
        "definition": "A standardized legal agreement to buy or sell an asset at a predetermined price at a specified time in the future.",
        "category": "Derivatives",
        "related_terms": ["forward contract", "margin", "mark-to-market", "settlement"],
    },
    "arbitrage": {
        "definition": "The simultaneous purchase and sale of the same or equivalent asset in different markets to profit from price discrepancies.",
        "category": "Trading",
        "related_terms": ["risk-free profit", "market efficiency", "spread", "convergence"],
    },
    "short_selling": {
        "definition": "The sale of a security that the seller has borrowed, with the intention of buying it back later at a lower price for a profit.",
        "category": "Trading",
        "related_terms": ["margin", "short squeeze", "borrow cost", "covering"],
    },
    "bull_market": {
        "definition": "A financial market condition in which prices are rising or expected to rise, typically defined as a 20% or more increase from recent lows.",
        "category": "Markets",
        "related_terms": ["bear market", "rally", "market cycle", "sentiment"],
    },
    "bear_market": {
        "definition": "A financial market condition in which prices are falling or expected to fall, typically defined as a 20% or more decline from recent highs.",
        "category": "Markets",
        "related_terms": ["bull market", "correction", "recession", "capitulation"],
    },
    "inflation": {
        "definition": "The rate at which the general level of prices for goods and services rises, eroding the purchasing power of money.",
        "category": "Economics",
        "related_terms": ["CPI", "deflation", "purchasing power", "real return", "TIPS"],
    },
    "gdp": {
        "definition": "Gross Domestic Product. The total monetary value of all finished goods and services produced within a country's borders in a specific time period.",
        "category": "Economics",
        "related_terms": ["GNP", "real GDP", "nominal GDP", "economic growth"],
    },
    "roi": {
        "definition": "Return on Investment. A performance measure calculated as (Net Profit / Cost of Investment) x 100, expressed as a percentage.",
        "category": "Valuation",
        "related_terms": ["IRR", "NPV", "payback period", "ROIC"],
    },
    "npv": {
        "definition": "Net Present Value. The difference between the present value of cash inflows and outflows over a period of time, used to evaluate investment profitability.",
        "category": "Valuation",
        "related_terms": ["IRR", "discount rate", "time value of money", "DCF"],
    },
    "irr": {
        "definition": "Internal Rate of Return. The discount rate that makes the net present value of all cash flows from an investment equal to zero.",
        "category": "Valuation",
        "related_terms": ["NPV", "hurdle rate", "WACC", "discount rate"],
    },
    "wacc": {
        "definition": "Weighted Average Cost of Capital. The average rate of return a company must earn on its existing assets to satisfy its creditors, owners, and other providers of capital.",
        "category": "Corporate Finance",
        "related_terms": ["cost of equity", "cost of debt", "capital structure", "discount rate"],
    },
    "dcf": {
        "definition": "Discounted Cash Flow. A valuation method that estimates the value of an investment based on its expected future cash flows, discounted to present value.",
        "category": "Valuation",
        "related_terms": ["NPV", "discount rate", "free cash flow", "terminal value"],
    },
    "etf": {
        "definition": "Exchange-Traded Fund. A type of investment fund traded on stock exchanges that holds assets such as stocks, bonds, or commodities.",
        "category": "Investing",
        "related_terms": ["mutual fund", "index fund", "NAV", "expense ratio"],
    },
    "mutual_fund": {
        "definition": "A pooled investment vehicle managed by professional fund managers that invests in stocks, bonds, or other securities on behalf of investors.",
        "category": "Investing",
        "related_terms": ["NAV", "expense ratio", "load", "prospectus", "ETF"],
    },
    "ipo": {
        "definition": "Initial Public Offering. The process through which a private company offers shares to the public for the first time on a stock exchange.",
        "category": "Corporate Finance",
        "related_terms": ["underwriter", "prospectus", "lock-up period", "SPAC", "direct listing"],
    },
}


def financial_term_glossary(term: str) -> dict[str, Any]:
    """Look up definitions, categories, and related terms for common financial terms."""
    try:
        key = term.lower().strip().replace(" ", "_").replace("-", "_")
        if key in _GLOSSARY:
            entry = _GLOSSARY[key]
            return {
                "status": "ok",
                "data": {
                    "term": term,
                    "definition": entry["definition"],
                    "category": entry["category"],
                    "related_terms": entry["related_terms"],
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        # Try partial match
        matches = [k for k in _GLOSSARY if key in k or k in key]
        if matches:
            entry = _GLOSSARY[matches[0]]
            return {
                "status": "ok",
                "data": {
                    "term": matches[0].replace("_", " "),
                    "definition": entry["definition"],
                    "category": entry["category"],
                    "related_terms": entry["related_terms"],
                    "note": f"Exact match for '{term}' not found. Showing closest match.",
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        available = sorted(_GLOSSARY.keys())
        return {
            "status": "error",
            "data": {
                "error": f"Term '{term}' not found in glossary.",
                "available_terms": [t.replace("_", " ") for t in available],
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
