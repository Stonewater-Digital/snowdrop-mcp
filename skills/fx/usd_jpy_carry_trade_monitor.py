"""
Executive Summary: Analyzes the USD/JPY carry trade attractiveness by comparing US Treasury yields with Japanese Government Bond (JGB) yields and factoring in FX volatility.
"""
from __future__ import annotations
from datetime import datetime, timezone
from skills.utils import log_lesson
from skills.data_ingestion.synthetic_market_data_generator import synthetic_market_data_generator

TOOL_META = {
    "name": "usd_jpy_carry_trade_monitor",
    "tier": "free",
    "description": "Analyzes USD/JPY carry trade profitability using US vs Japan yield differentials and synthetic FX volatility.",
}

def usd_jpy_carry_trade_monitor(us_10y_yield: float | None = None, jp_10y_yield: float | None = None) -> dict:
    """Evaluate the USD/JPY carry trade setup.
    
    Args:
        us_10y_yield: Optional live US 10-year yield. If None, synthetic data is used.
        jp_10y_yield: Optional live JP 10-year yield. If None, synthetic data is used.
    """
    try:
        ts = datetime.now(timezone.utc)
        
        # Use synthetic data fallback if live rates not provided
        if us_10y_yield is None:
            synth_us = synthetic_market_data_generator("rates", "time_series", days_back=1)
            us_10y_yield = synth_us["data"]["series"][-1]["price"] if synth_us.get("status") == "success" else 4.25
            
        if jp_10y_yield is None:
            synth_jp = synthetic_market_data_generator("rates", "time_series", days_back=1)
            jp_10y_yield = (synth_jp["data"]["series"][-1]["price"] * 0.1) if synth_jp.get("status") == "success" else 0.85

        yield_differential = us_10y_yield - jp_10y_yield
        
        # Synthetic FX vol
        synth_fx = synthetic_market_data_generator("fx", "volatility_surface")
        fx_vol = synth_fx["data"].get("mock_value", 12.5) / 100.0 if synth_fx.get("status") == "success" else 0.10
        
        # Carry-to-Risk ratio (Differential / Annualized FX Volatility)
        carry_to_risk = yield_differential / (fx_vol * 100) if fx_vol > 0 else 0
        
        return {
            "status": "success",
            "data": {
                "us_10y_yield_pct": round(us_10y_yield, 3),
                "jp_10y_yield_pct": round(jp_10y_yield, 3),
                "yield_differential_bps": round(yield_differential * 100, 1),
                "implied_fx_volatility_pct": round(fx_vol * 100, 2),
                "carry_to_risk_ratio": round(carry_to_risk, 3),
                "trade_status": "Attractive" if carry_to_risk > 0.4 else "Crowded/Risky",
                "data_source": "synthetic fallback" if (us_10y_yield == 4.25 or jp_10y_yield == 0.85) else "user_provided"
            },
            "timestamp": ts.isoformat()
        }
    except Exception as e:
        log_lesson(f"usd_jpy_carry_trade_monitor: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
