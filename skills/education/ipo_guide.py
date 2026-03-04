"""Educational guide to Initial Public Offerings (IPOs).

MCP Tool Name: ipo_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ipo_guide",
    "description": "Returns educational content on IPOs: process, underwriting, lock-up period, pricing, direct listing, and SPACs.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def ipo_guide() -> dict[str, Any]:
    """Returns educational content on Initial Public Offerings."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "An Initial Public Offering (IPO) is the process by which a private company offers shares to the public for the first time, transitioning from private to public ownership. It allows the company to raise capital from public investors and gives early stakeholders liquidity.",
                "key_concepts": [
                    "IPOs are a major milestone — the company becomes subject to public reporting requirements (SEC filings)",
                    "The IPO price and the opening trading price are often very different",
                    "Early investors and employees face lock-up restrictions on selling",
                    "Most IPOs underperform the broader market over 3-5 years after listing",
                ],
                "process": {
                    "step_1_selection": "The company selects one or more investment banks as underwriters to manage the IPO process.",
                    "step_2_due_diligence": "Underwriters conduct extensive due diligence and help the company prepare financial statements and disclosures.",
                    "step_3_sec_filing": "The company files a registration statement (S-1) with the SEC, including a prospectus with financial data, risk factors, and use of proceeds.",
                    "step_4_roadshow": "Management presents to institutional investors to generate interest and gauge demand. Typically 1-2 weeks of meetings across major cities.",
                    "step_5_pricing": "Based on roadshow feedback and market conditions, the underwriters and company set the final IPO price the night before trading begins.",
                    "step_6_trading": "Shares begin trading on a stock exchange (NYSE or Nasdaq). The opening price is determined by market supply and demand.",
                },
                "underwriting": {
                    "role": "Investment banks that manage the IPO process, guarantee a minimum amount of capital raised, and distribute shares to institutional investors.",
                    "types": {
                        "firm_commitment": "Underwriters buy all shares from the company and resell to investors. Most common for large IPOs. Company is guaranteed the proceeds.",
                        "best_efforts": "Underwriters agree to sell as many shares as possible but do not guarantee all will be sold. Used for riskier or smaller offerings.",
                    },
                    "fees": "Underwriting spread (commission) is typically 3-7% of total proceeds. A $1 billion IPO might pay $50-70 million in fees.",
                    "stabilization": "Underwriters may buy shares in the open market to support the stock price in the days following the IPO (greenshoe option).",
                },
                "lock_up_period": {
                    "definition": "A contractual restriction (typically 90-180 days) preventing insiders, employees, and early investors from selling their shares after the IPO.",
                    "purpose": "Prevents a flood of insider selling immediately after the IPO, which could tank the stock price.",
                    "expiration_impact": "When the lock-up expires, a significant increase in available shares can create selling pressure and price declines.",
                },
                "pricing": {
                    "ipo_price": "Set by the underwriters based on company valuation, comparable companies, market conditions, and investor demand from the roadshow.",
                    "underpricing": "IPOs are frequently priced 10-20% below the expected market value, benefiting initial institutional buyers. This 'IPO pop' on the first day represents money left on the table by the company.",
                    "first_day_return": "The average first-day return for U.S. IPOs has historically been around 15-20%. However, individual IPOs vary wildly.",
                },
                "alternatives": {
                    "direct_listing": {
                        "definition": "The company lists existing shares directly on an exchange without issuing new shares or using underwriters. No new capital is raised.",
                        "advantages": "No dilution, no underwriting fees, no lock-up period, market-determined pricing.",
                        "disadvantages": "No guaranteed capital raise, no price stabilization, less marketing/roadshow support.",
                    },
                    "spac": {
                        "definition": "A Special Purpose Acquisition Company (SPAC) is a shell company that raises money through its own IPO with the sole purpose of acquiring a private company, effectively taking it public through a reverse merger.",
                        "advantages": "Faster process, more pricing certainty, ability to share forward projections (not allowed in traditional IPOs).",
                        "disadvantages": "Dilution from sponsor shares (typically 20%), warrants dilution, potential conflicts of interest, historically poor post-merger returns.",
                    },
                },
                "example": "A tech company files an S-1 showing $500M revenue growing 40% annually. Underwriters propose a $20-$22 price range. After a successful roadshow with strong demand, the IPO is priced at $24 (above range). On the first trading day, shares open at $32 and close at $30 — a 25% first-day pop. The company raised $2.4 billion (100M shares * $24).",
                "common_mistakes": [
                    "Buying IPOs on the first day at inflated prices (the 'pop' benefits institutional investors who got the IPO price, not retail buyers)",
                    "Ignoring the lock-up expiration date and the potential selling pressure it creates",
                    "Assuming all IPOs are good investments — most underperform the market over 3-5 years",
                    "Not reading the S-1 prospectus, especially risk factors and use of proceeds",
                    "FOMO buying based on hype without understanding the company's fundamentals and valuation",
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
