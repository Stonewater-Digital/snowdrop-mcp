"""Educational guide to monetary policy and central banking.

MCP Tool Name: monetary_policy_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "monetary_policy_guide",
    "description": "Returns educational content on monetary policy: Fed tools, interest rates, quantitative easing, and inflation targeting.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def monetary_policy_guide() -> dict[str, Any]:
    """Returns educational content on monetary policy."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "Monetary policy refers to the actions taken by a central bank (such as the Federal Reserve in the U.S.) to manage the money supply and interest rates in order to achieve macroeconomic objectives: stable prices, maximum employment, and moderate long-term interest rates.",
                "key_concepts": [
                    "The Federal Reserve is the central bank of the United States, established in 1913",
                    "Monetary policy operates through the banking system and financial markets",
                    "Policy changes affect the economy with a lag of 6-18 months",
                    "The Fed has a dual mandate: price stability and maximum employment",
                ],
                "fed_tools": {
                    "federal_funds_rate": "The target overnight lending rate between banks. The Fed's primary policy tool. Raising the rate tightens monetary conditions; lowering it eases them. The FOMC sets this target at eight meetings per year.",
                    "open_market_operations": "The buying and selling of U.S. Treasury securities. Buying bonds injects money into the banking system (expansionary). Selling bonds withdraws money (contractionary). The most frequently used tool.",
                    "discount_rate": "The interest rate charged to commercial banks for borrowing directly from the Fed's discount window. Usually set above the federal funds rate. Used as a safety valve for banks needing emergency liquidity.",
                    "reserve_requirements": "The fraction of deposits banks must hold as reserves (historically 0-10%). Set to 0% in March 2020. Higher requirements reduce lending capacity; lower requirements increase it.",
                },
                "interest_rates": {
                    "transmission_mechanism": "Changes in the fed funds rate ripple through the economy: affecting prime rate, mortgage rates, auto loans, credit cards, corporate borrowing, savings rates, and ultimately spending and investment decisions.",
                    "raising_rates": "Tightening policy. Makes borrowing more expensive, slowing spending and investment. Used to combat inflation. Strengthens the dollar. Negative for bond prices.",
                    "lowering_rates": "Easing policy. Makes borrowing cheaper, stimulating spending and investment. Used to combat recession and unemployment. Weakens the dollar. Positive for bond prices.",
                    "zero_lower_bound": "When rates reach near-zero, conventional policy loses effectiveness. The Fed turns to unconventional tools like QE and forward guidance.",
                },
                "quantitative_easing": {
                    "definition": "Large-scale asset purchases by the central bank to inject liquidity into the financial system when interest rates are already near zero.",
                    "how_it_works": "The Fed creates new bank reserves (electronically) and uses them to buy Treasury bonds and mortgage-backed securities from banks, pushing down long-term interest rates and encouraging lending.",
                    "quantitative_tightening": "The reverse process — the Fed lets bonds mature without reinvesting or actively sells them, reducing the money supply and its balance sheet.",
                    "history": "QE1 (2008-2010), QE2 (2010-2011), QE3 (2012-2014) during the financial crisis. QE resumed in 2020 during COVID-19.",
                },
                "inflation_targeting": {
                    "target": "The Fed targets 2% annual inflation (measured by PCE) as consistent with price stability. Below 2% risks deflation; significantly above 2% erodes purchasing power.",
                    "average_inflation_targeting": "Adopted in 2020, this framework allows inflation to run moderately above 2% after periods of undershooting, aiming for 2% on average over time.",
                    "forward_guidance": "Communication about the likely future path of monetary policy. Aims to influence long-term interest rates and economic expectations by telling markets what the Fed intends to do.",
                },
                "example": "When inflation rises to 5%, the Fed raises the federal funds rate in 0.25-0.75% increments over multiple meetings. Higher rates increase mortgage rates (reducing housing demand), increase corporate borrowing costs (reducing investment), and strengthen the dollar (reducing import prices), all working to slow inflation.",
                "common_mistakes": [
                    "Assuming the Fed directly controls mortgage rates and long-term rates (it sets the short-term fed funds rate; markets set longer rates)",
                    "Expecting immediate economic effects from rate changes (monetary policy works with long and variable lags)",
                    "Confusing money printing with QE (QE creates bank reserves, not cash in circulation)",
                    "Ignoring that the Fed must balance inflation and employment, which sometimes conflict",
                    "Assuming rate cuts are always positive for stocks (rate cuts signal economic weakness)",
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
