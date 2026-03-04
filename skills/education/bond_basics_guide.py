"""Educational guide to bond fundamentals including types, key terms, and pricing basics.

MCP Tool Name: bond_basics_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "bond_basics_guide",
    "description": "Returns educational content on bond fundamentals: definition, types, key terms, and pricing basics.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def bond_basics_guide() -> dict[str, Any]:
    """Returns educational content on bond fundamentals."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "A bond is a fixed-income debt instrument representing a loan from an investor to a borrower (typically a corporation or government). The issuer promises to pay periodic interest (coupon) and return the principal (face value) at maturity.",
                "key_concepts": [
                    "Bonds are debt instruments, not equity — bondholders are creditors, not owners",
                    "Bond prices and interest rates move inversely",
                    "Credit quality determines the risk premium (spread) over risk-free rates",
                    "Bonds can be traded on secondary markets before maturity",
                ],
                "types": {
                    "treasury_bonds": "Issued by the U.S. federal government. Considered risk-free for default. Maturities: T-Bills (<1yr), T-Notes (2-10yr), T-Bonds (20-30yr).",
                    "corporate_bonds": "Issued by companies to raise capital. Higher yields than treasuries to compensate for credit risk. Rated by agencies (Moody's, S&P, Fitch).",
                    "municipal_bonds": "Issued by state/local governments. Interest often exempt from federal (and sometimes state) income tax. Two types: general obligation and revenue bonds.",
                    "agency_bonds": "Issued by government-sponsored enterprises (Fannie Mae, Freddie Mac). Slightly higher yield than treasuries with implicit government backing.",
                    "high_yield_bonds": "Also called junk bonds. Rated below BBB-/Baa3. Higher default risk compensated by significantly higher yields.",
                    "zero_coupon_bonds": "Sold at a discount to face value with no periodic coupon payments. Return comes entirely from the difference between purchase price and face value at maturity.",
                },
                "key_terms": {
                    "coupon_rate": "The annual interest rate paid on the bond's face value. A $1,000 bond with 5% coupon pays $50/year.",
                    "yield_to_maturity": "The total annualized return if the bond is held until maturity, accounting for coupon payments, current price, and time to maturity.",
                    "current_yield": "Annual coupon payment divided by the bond's current market price.",
                    "maturity": "The date when the bond's principal (face value) is repaid to the investor.",
                    "duration": "A measure of a bond's price sensitivity to interest rate changes. Higher duration means more price volatility when rates change.",
                    "face_value": "The par value of the bond, typically $1,000, returned to the investor at maturity.",
                    "credit_rating": "An assessment of the issuer's ability to repay. Investment grade: AAA to BBB-. Speculative: BB+ and below.",
                    "call_provision": "Allows the issuer to redeem the bond before maturity, typically when interest rates fall.",
                },
                "pricing_basics": {
                    "par": "Bond trading at face value (price = 100). Coupon rate equals market yield.",
                    "premium": "Bond trading above face value (price > 100). Coupon rate exceeds current market yield.",
                    "discount": "Bond trading below face value (price < 100). Coupon rate is below current market yield.",
                    "price_formula": "Bond price = Present value of all future coupon payments + Present value of face value at maturity.",
                    "inverse_relationship": "When market interest rates rise, existing bond prices fall (and vice versa) because new bonds offer higher coupons.",
                },
                "common_mistakes": [
                    "Confusing coupon rate with yield to maturity",
                    "Ignoring interest rate risk for long-duration bonds",
                    "Assuming all bonds are safe — corporate and high-yield bonds carry real default risk",
                    "Not considering inflation's impact on real returns from fixed coupon payments",
                    "Overlooking call risk — callable bonds may be redeemed early when rates drop",
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
