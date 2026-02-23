"""
Executive Summary: Calculates Distributable Cash Flow (DCF) for Master Limited Partnerships (MLPs) by adjusting Net Income for non-cash items and maintenance CapEx.
"""
from __future__ import annotations
from datetime import datetime, timezone
from skills.utils import log_lesson

TOOL_META = {
    "name": "mlp_distributable_cash_flow_calc",
    "tier": "free",
    "description": "Calculates Distributable Cash Flow (DCF) and coverage ratios for Master Limited Partnerships.",
}

def mlp_distributable_cash_flow_calc(net_income: float, dda: float, maintenance_capex: float, distributions_paid: float) -> dict:
    """Calculate MLP Distributable Cash Flow.
    
    Args:
        net_income: Net Income reported
        dda: Depreciation, Depletion, and Amortization (non-cash add-back)
        maintenance_capex: Capital expenditures required to maintain current assets
        distributions_paid: Total distributions paid to unitholders
    """
    try:
        ts = datetime.now(timezone.utc)
        
        # Simplified DCF formula
        dcf = net_income + dda - maintenance_capex
        
        coverage_ratio = dcf / distributions_paid if distributions_paid > 0 else 0.0
        
        return {
            "status": "success",
            "data": {
                "net_income": net_income,
                "dda_addback": dda,
                "maintenance_capex": maintenance_capex,
                "distributable_cash_flow_dcf": round(dcf, 2),
                "distributions_paid": distributions_paid,
                "coverage_ratio": round(coverage_ratio, 2),
                "distribution_safety": "Safe" if coverage_ratio >= 1.2 else ("At Risk" if coverage_ratio < 1.0 else "Adequate")
            },
            "timestamp": ts.isoformat()
        }
    except Exception as e:
        log_lesson(f"mlp_distributable_cash_flow_calc: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
