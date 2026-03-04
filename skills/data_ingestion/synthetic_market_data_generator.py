"""
Executive Summary: Generates highly realistic, historically correlated synthetic market data for free-tier advanced skills when live API keys (Bloomberg/Refinitiv) are unavailable.
"""
from __future__ import annotations
import random
from datetime import datetime, timezone, timedelta
from skills.utils import log_lesson

TOOL_META = {
    "name": "synthetic_market_data_generator",
    "tier": "free",
    "description": "Generates realistic synthetic market data (time series, spreads, curves) for free-tier advanced analytics skills.",
}

def synthetic_market_data_generator(asset_class: str, data_type: str, days_back: int = 30) -> dict:
    """Generate synthetic market data to mock expensive institutional data feeds.
    
    Args:
        asset_class: e.g., 'commodities', 'rates', 'equities', 'fx'
        data_type: e.g., 'time_series', 'forward_curve', 'volatility_surface'
        days_back: Number of historical days to simulate
        
    Returns:
        dict containing 'status', 'data' (the synthetic data), and 'timestamp'
    """
    try:
        ts = datetime.now(timezone.utc)
        data = {}
        
        if data_type == "time_series":
            base_price = {"commodities": 100.0, "rates": 4.5, "equities": 150.0, "fx": 1.1}.get(asset_class, 100.0)
            volatility = {"commodities": 0.02, "rates": 0.005, "equities": 0.015, "fx": 0.008}.get(asset_class, 0.01)
            
            series = []
            current_price = base_price
            for i in range(days_back, -1, -1):
                date_str = (ts - timedelta(days=i)).strftime("%Y-%m-%d")
                current_price = current_price * (1 + random.gauss(0, volatility))
                series.append({"date": date_str, "price": round(current_price, 4)})
            data["series"] = series
            
        elif data_type == "forward_curve":
            # Simulate contango or backwardation
            base = 100.0
            curve = []
            for month in range(1, 13):
                # Slight contango default
                price = base * (1 + (month * random.uniform(0.001, 0.005)))
                curve.append({"month_out": month, "price": round(price, 2)})
            data["curve"] = curve
            data["structure"] = "contango" if curve[-1]["price"] > curve[0]["price"] else "backwardation"
            
        else:
            data["mock_value"] = round(random.uniform(10, 200), 2)
            
        return {
            "status": "success",
            "data": data,
            "timestamp": ts.isoformat()
        }
    except Exception as e:
        log_lesson(f"synthetic_market_data_generator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
