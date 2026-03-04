"""Look up interpretation guides for common financial ratios.

MCP Tool Name: ratio_interpretation_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ratio_interpretation_guide",
    "description": "Returns definition, formula, healthy range, and interpretation for 15+ financial ratios.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "ratio_name": {
                "type": "string",
                "description": "The name of the financial ratio to look up.",
            },
        },
        "required": ["ratio_name"],
    },
}

_RATIOS: dict[str, dict[str, Any]] = {
    "current_ratio": {
        "definition": "Measures a company's ability to pay short-term obligations with its current assets.",
        "formula": "Current Assets / Current Liabilities",
        "healthy_range": "1.5 - 3.0",
        "interpretation": "Above 1 means the company can cover short-term debts. Below 1 signals potential liquidity problems. Too high (>3) may indicate inefficient use of assets.",
    },
    "quick_ratio": {
        "definition": "A stricter liquidity measure that excludes inventory from current assets.",
        "formula": "(Current Assets - Inventory) / Current Liabilities",
        "healthy_range": "1.0 - 2.0",
        "interpretation": "Above 1 means the company can meet short-term obligations without selling inventory. More conservative than the current ratio.",
    },
    "debt_to_equity": {
        "definition": "Measures the proportion of debt financing relative to shareholder equity.",
        "formula": "Total Liabilities / Shareholders' Equity",
        "healthy_range": "0.5 - 1.5 (varies by industry)",
        "interpretation": "Higher ratios indicate more leverage and financial risk. Capital-intensive industries (utilities, real estate) naturally carry higher D/E. Below 1.0 is generally conservative.",
    },
    "debt_to_assets": {
        "definition": "Shows the percentage of a company's assets financed by debt.",
        "formula": "Total Liabilities / Total Assets",
        "healthy_range": "0.3 - 0.6",
        "interpretation": "Higher values mean more assets are funded by debt, increasing financial risk. Values above 0.6 may signal over-leverage.",
    },
    "gross_margin": {
        "definition": "The percentage of revenue remaining after deducting cost of goods sold.",
        "formula": "(Revenue - COGS) / Revenue * 100",
        "healthy_range": "20% - 80% (highly industry dependent)",
        "interpretation": "Higher margins indicate better pricing power and production efficiency. Software companies often exceed 70%; retail/grocery may be 25-35%.",
    },
    "operating_margin": {
        "definition": "The percentage of revenue remaining after deducting operating expenses.",
        "formula": "Operating Income / Revenue * 100",
        "healthy_range": "10% - 30%",
        "interpretation": "Indicates how efficiently a company manages its operations. Higher is better. Declining margins may signal rising costs or pricing pressure.",
    },
    "net_profit_margin": {
        "definition": "The percentage of revenue that translates into net profit after all expenses.",
        "formula": "Net Income / Revenue * 100",
        "healthy_range": "5% - 20% (industry dependent)",
        "interpretation": "The bottom-line profitability measure. Compares across competitors within the same industry for meaningful analysis.",
    },
    "return_on_equity": {
        "definition": "Measures how effectively a company uses shareholder equity to generate profit.",
        "formula": "Net Income / Shareholders' Equity * 100",
        "healthy_range": "15% - 25%",
        "interpretation": "Higher ROE indicates better capital efficiency. Compare within industries. Very high ROE with high debt may be misleading. Use DuPont analysis for deeper insight.",
    },
    "return_on_assets": {
        "definition": "Measures how efficiently a company uses its total assets to generate profit.",
        "formula": "Net Income / Total Assets * 100",
        "healthy_range": "5% - 15%",
        "interpretation": "Asset-light businesses (tech) typically have higher ROA than asset-heavy ones (manufacturing). Compare within the same sector.",
    },
    "price_to_earnings": {
        "definition": "Compares a company's current share price to its earnings per share.",
        "formula": "Market Price per Share / Earnings per Share",
        "healthy_range": "15 - 25 (market average ~20)",
        "interpretation": "Higher P/E suggests investors expect higher growth. Very high P/E may indicate overvaluation. Use forward P/E for growth companies. Compare within sectors.",
    },
    "price_to_book": {
        "definition": "Compares market value to book value, indicating how much investors pay per dollar of net assets.",
        "formula": "Market Price per Share / Book Value per Share",
        "healthy_range": "1.0 - 3.0",
        "interpretation": "Below 1 may indicate undervaluation or fundamental problems. Above 3 suggests investors see significant intangible value or growth potential.",
    },
    "price_to_sales": {
        "definition": "Valuation ratio comparing share price to revenue per share.",
        "formula": "Market Cap / Annual Revenue",
        "healthy_range": "1.0 - 5.0",
        "interpretation": "Useful for companies with no earnings. Lower P/S may signal undervaluation. High-growth SaaS companies often trade at 10-30x sales.",
    },
    "inventory_turnover": {
        "definition": "Measures how many times inventory is sold and replaced over a period.",
        "formula": "Cost of Goods Sold / Average Inventory",
        "healthy_range": "5 - 10 (industry dependent)",
        "interpretation": "Higher turnover means faster inventory movement and better efficiency. Low turnover may indicate overstocking or obsolescence. Grocery: 15+; luxury goods: 2-4.",
    },
    "receivables_turnover": {
        "definition": "Measures how efficiently a company collects its accounts receivable.",
        "formula": "Net Credit Sales / Average Accounts Receivable",
        "healthy_range": "6 - 12",
        "interpretation": "Higher ratio means faster collection. Low ratio may signal collection issues or overly generous credit terms. Convert to days: 365 / turnover ratio.",
    },
    "interest_coverage": {
        "definition": "Measures a company's ability to pay interest on its outstanding debt.",
        "formula": "EBIT / Interest Expense",
        "healthy_range": "3.0 - 10.0+",
        "interpretation": "Below 1.5 is a warning sign. Below 1.0 means the company cannot cover interest payments from operating income. Higher is safer for creditors.",
    },
    "dividend_yield": {
        "definition": "The annual dividend payment expressed as a percentage of the stock's current price.",
        "formula": "Annual Dividends per Share / Price per Share * 100",
        "healthy_range": "2% - 5%",
        "interpretation": "Very high yields (>6%) may signal a stock price decline or unsustainable payout. Low yield may indicate a growth-oriented company reinvesting profits.",
    },
    "payout_ratio": {
        "definition": "The proportion of earnings paid out as dividends to shareholders.",
        "formula": "Dividends per Share / Earnings per Share * 100",
        "healthy_range": "30% - 60%",
        "interpretation": "Above 100% means the company is paying more in dividends than it earns, which is unsustainable long-term. REITs typically have 80-90% payout ratios by design.",
    },
    "free_cash_flow_yield": {
        "definition": "Compares free cash flow per share to the market price per share.",
        "formula": "Free Cash Flow per Share / Market Price per Share * 100",
        "healthy_range": "4% - 8%",
        "interpretation": "Higher yield suggests the stock may be undervalued relative to its cash generation. More reliable than earnings-based metrics as it's harder to manipulate.",
    },
}


def ratio_interpretation_guide(ratio_name: str) -> dict[str, Any]:
    """Returns definition, formula, healthy range, and interpretation for financial ratios."""
    try:
        key = ratio_name.lower().strip().replace(" ", "_").replace("-", "_")
        if key in _RATIOS:
            entry = _RATIOS[key]
            return {
                "status": "ok",
                "data": {
                    "ratio_name": ratio_name,
                    "definition": entry["definition"],
                    "formula": entry["formula"],
                    "healthy_range": entry["healthy_range"],
                    "interpretation": entry["interpretation"],
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        matches = [k for k in _RATIOS if key in k or k in key]
        if matches:
            entry = _RATIOS[matches[0]]
            return {
                "status": "ok",
                "data": {
                    "ratio_name": matches[0].replace("_", " "),
                    "definition": entry["definition"],
                    "formula": entry["formula"],
                    "healthy_range": entry["healthy_range"],
                    "interpretation": entry["interpretation"],
                    "note": f"Exact match for '{ratio_name}' not found. Showing closest match.",
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        available = sorted(_RATIOS.keys())
        return {
            "status": "error",
            "data": {
                "error": f"Ratio '{ratio_name}' not found.",
                "available_ratios": [r.replace("_", " ") for r in available],
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
