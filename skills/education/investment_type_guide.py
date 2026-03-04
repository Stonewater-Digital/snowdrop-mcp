"""Overview of major investment types with risk and return profiles.

MCP Tool Name: investment_type_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "investment_type_guide",
    "description": "Returns overview of major investment types (stocks, bonds, mutual funds, ETFs, real estate, commodities) with risk/return profiles.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "investment_type": {
                "type": "string",
                "description": "Optional specific investment type to look up. If omitted, returns all types.",
            },
        },
        "required": [],
    },
}

_TYPES: dict[str, dict[str, Any]] = {
    "stocks": {
        "definition": "Ownership shares in a publicly traded company, representing a claim on the company's assets and earnings.",
        "risk_level": "Moderate to High",
        "historical_return": "~10% annualized (S&P 500 long-term average, nominal)",
        "liquidity": "High (traded on exchanges during market hours)",
        "minimum_investment": "Price of one share (fractional shares available at many brokers)",
        "pros": ["High long-term growth potential", "Dividend income", "Easy to buy/sell", "Ownership stake in companies"],
        "cons": ["Price volatility", "Company-specific risk", "Requires research/analysis", "Emotional decision-making risk"],
        "best_for": "Long-term growth investors with tolerance for short-term volatility.",
    },
    "bonds": {
        "definition": "Fixed-income debt securities where the investor lends money to an issuer (government or corporation) in exchange for periodic interest and return of principal at maturity.",
        "risk_level": "Low to Moderate",
        "historical_return": "~4-6% annualized (varies by type and credit quality)",
        "liquidity": "Moderate (some trade on exchanges; many trade OTC)",
        "minimum_investment": "$1,000 face value typical; bond funds allow smaller amounts",
        "pros": ["Predictable income stream", "Lower volatility than stocks", "Portfolio diversification", "Capital preservation"],
        "cons": ["Interest rate risk", "Inflation risk erodes real returns", "Credit/default risk", "Lower long-term returns than stocks"],
        "best_for": "Income-focused investors and those seeking portfolio stability.",
    },
    "mutual_funds": {
        "definition": "Professionally managed pooled investment vehicles that collect money from many investors to buy a diversified portfolio of securities.",
        "risk_level": "Varies (depends on fund strategy)",
        "historical_return": "Varies by fund type; equity funds average ~8-10%",
        "liquidity": "Moderate (redeemed at end-of-day NAV)",
        "minimum_investment": "$500 - $3,000 typical minimums",
        "pros": ["Professional management", "Instant diversification", "Regulated and transparent", "Automatic reinvestment options"],
        "cons": ["Management fees (expense ratios)", "No intraday trading", "Potential tax inefficiency", "Some have sales loads"],
        "best_for": "Investors wanting professional management and diversification with moderate minimums.",
    },
    "etfs": {
        "definition": "Exchange-Traded Funds that hold baskets of securities and trade on stock exchanges like individual stocks throughout the day.",
        "risk_level": "Varies (depends on underlying holdings)",
        "historical_return": "Varies; index ETFs track their benchmark index",
        "liquidity": "High (traded on exchanges during market hours)",
        "minimum_investment": "Price of one share (fractional shares available)",
        "pros": ["Low expense ratios", "Intraday trading", "Tax efficient", "Wide variety of strategies"],
        "cons": ["Brokerage commissions (though many are now free)", "Bid-ask spread costs", "Some niche ETFs have low volume", "Can trade at premium/discount to NAV"],
        "best_for": "Cost-conscious investors wanting diversification with trading flexibility.",
    },
    "real_estate": {
        "definition": "Physical property or financial instruments (REITs) that derive value from land and buildings, generating returns through rental income and appreciation.",
        "risk_level": "Moderate",
        "historical_return": "~8-12% annualized (including rental income and appreciation)",
        "liquidity": "Low (physical property) to High (REITs)",
        "minimum_investment": "Tens of thousands (physical) or share price (REITs/crowdfunding)",
        "pros": ["Tangible asset", "Rental income stream", "Inflation hedge", "Tax benefits (depreciation, 1031 exchange)"],
        "cons": ["Illiquidity (physical property)", "High transaction costs", "Management burden", "Concentration risk"],
        "best_for": "Investors seeking income, inflation protection, and portfolio diversification.",
    },
    "commodities": {
        "definition": "Raw materials or primary agricultural products (gold, oil, wheat, etc.) that can be traded, typically through futures contracts or commodity ETFs.",
        "risk_level": "High",
        "historical_return": "~3-5% annualized (highly variable)",
        "liquidity": "Moderate to High (futures markets and commodity ETFs)",
        "minimum_investment": "Varies; ETFs allow small positions; futures require margin accounts",
        "pros": ["Inflation hedge", "Portfolio diversification", "Low correlation with stocks/bonds", "Tangible value"],
        "cons": ["No income generation", "High volatility", "Storage costs (physical)", "Contango risk in futures"],
        "best_for": "Investors seeking inflation protection and portfolio diversification with high risk tolerance.",
    },
}


def investment_type_guide(investment_type: str = "") -> dict[str, Any]:
    """Returns overview of investment types with risk/return profiles."""
    try:
        if not investment_type:
            summary = {}
            for name, info in _TYPES.items():
                summary[name] = {
                    "definition": info["definition"],
                    "risk_level": info["risk_level"],
                    "historical_return": info["historical_return"],
                    "best_for": info["best_for"],
                }
            return {
                "status": "ok",
                "data": {
                    "investment_types": summary,
                    "total_types": len(summary),
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        key = investment_type.lower().strip().replace(" ", "_").replace("-", "_")
        if key in _TYPES:
            return {
                "status": "ok",
                "data": {"investment_type": key, **_TYPES[key]},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        matches = [k for k in _TYPES if key in k or k in key]
        if matches:
            best = matches[0]
            return {
                "status": "ok",
                "data": {
                    "investment_type": best,
                    **_TYPES[best],
                    "note": f"Exact match for '{investment_type}' not found. Showing closest match.",
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        return {
            "status": "error",
            "data": {
                "error": f"Investment type '{investment_type}' not found.",
                "available_types": sorted(_TYPES.keys()),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
