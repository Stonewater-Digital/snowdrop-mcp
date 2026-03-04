"""Fetch the current gold price.

MCP Tool Name: gold_price_fetcher
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import os

TOOL_META: dict[str, Any] = {
    "name": "gold_price_fetcher",
    "description": "Fetch the current gold price per troy ounce in USD. Tries metals.dev API or returns recent reference price.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def gold_price_fetcher() -> dict[str, Any]:
    """Fetch the current gold price."""
    try:
        import httpx

        # Try free metals API
        price = None
        source = "reference"
        api_data = {}

        try:
            # Try metals.dev free API
            with httpx.Client(timeout=15) as client:
                resp = client.get("https://api.metals.dev/v1/latest?api_key=demo&currency=USD&unit=toz")
                if resp.status_code == 200:
                    data = resp.json()
                    metals = data.get("metals", {})
                    if "gold" in metals:
                        price = metals["gold"]
                        source = "metals.dev"
                        api_data = data
        except Exception:
            pass

        if price is None:
            # Try FRED series GOLDAMGBD228NLBM (London gold fixing)
            fred_key = os.environ.get("FRED_API_KEY", "")
            if fred_key:
                try:
                    with httpx.Client(timeout=15) as client:
                        resp = client.get(
                            "https://api.stlouisfed.org/fred/series/observations",
                            params={
                                "series_id": "GOLDAMGBD228NLBM",
                                "api_key": fred_key,
                                "file_type": "json",
                                "sort_order": "desc",
                                "limit": "5",
                            },
                        )
                        if resp.status_code == 200:
                            obs = resp.json().get("observations", [])
                            for o in obs:
                                if o["value"] != ".":
                                    price = float(o["value"])
                                    source = "fred"
                                    break
                except Exception:
                    pass

        if price is None:
            # Hardcoded reference price as last resort
            price = 2950.00
            source = "hardcoded_reference"

        return {
            "status": "ok",
            "data": {
                "gold_price_usd_per_oz": round(price, 2),
                "unit": "USD per troy ounce",
                "source": source,
                "note": "Gold price per troy ounce. "
                + (
                    "Live price from API."
                    if source in ("metals.dev", "fred")
                    else "Reference price — may not reflect current market. Set FRED_API_KEY for live data."
                ),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
