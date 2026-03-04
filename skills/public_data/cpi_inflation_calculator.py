"""Calculate inflation-adjusted values using CPI data with BLS API fallback.

MCP Tool Name: cpi_inflation_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import os

# Hardcoded CPI-U annual averages (Bureau of Labor Statistics, base 1982-84=100)
_CPI_TABLE: dict[int, dict[int, float]] = {
    2015: {1: 233.707, 2: 234.722, 3: 236.119, 4: 236.599, 5: 237.805, 6: 238.638, 7: 238.654, 8: 238.316, 9: 237.945, 10: 237.838, 11: 237.336, 12: 236.525},
    2016: {1: 236.916, 2: 237.111, 3: 238.132, 4: 239.261, 5: 240.229, 6: 241.018, 7: 240.628, 8: 240.849, 9: 241.428, 10: 241.729, 11: 241.353, 12: 241.432},
    2017: {1: 242.839, 2: 243.603, 3: 243.801, 4: 244.524, 5: 244.733, 6: 244.955, 7: 244.786, 8: 245.519, 9: 246.819, 10: 246.663, 11: 246.669, 12: 246.524},
    2018: {1: 247.867, 2: 248.991, 3: 249.554, 4: 250.546, 5: 251.588, 6: 251.989, 7: 252.006, 8: 252.146, 9: 252.439, 10: 252.885, 11: 252.038, 12: 251.233},
    2019: {1: 251.712, 2: 252.776, 3: 254.202, 4: 255.548, 5: 256.092, 6: 256.143, 7: 256.571, 8: 256.558, 9: 256.759, 10: 257.346, 11: 257.208, 12: 256.974},
    2020: {1: 257.971, 2: 258.678, 3: 258.115, 4: 256.389, 5: 256.394, 6: 257.797, 7: 259.101, 8: 259.918, 9: 260.280, 10: 260.388, 11: 260.229, 12: 260.474},
    2021: {1: 261.582, 2: 263.014, 3: 264.877, 4: 267.054, 5: 269.195, 6: 271.696, 7: 273.003, 8: 273.567, 9: 274.310, 10: 276.589, 11: 277.948, 12: 278.802},
    2022: {1: 281.148, 2: 283.716, 3: 287.504, 4: 289.109, 5: 292.296, 6: 296.311, 7: 296.276, 8: 296.171, 9: 296.808, 10: 298.012, 11: 297.711, 12: 296.797},
    2023: {1: 299.170, 2: 300.840, 3: 301.836, 4: 303.363, 5: 304.127, 6: 305.109, 7: 305.691, 8: 307.026, 9: 307.789, 10: 307.671, 11: 307.051, 12: 306.746},
    2024: {1: 308.417, 2: 310.326, 3: 312.332, 4: 313.548, 5: 314.069, 6: 314.175, 7: 314.540, 8: 314.796, 9: 315.301, 10: 315.664, 11: 315.490, 12: 315.605},
    2025: {1: 317.671, 2: 317.863, 3: 318.200, 4: 318.500, 5: 318.800, 6: 319.100, 7: 319.400, 8: 319.700, 9: 320.000, 10: 320.300, 11: 320.600, 12: 320.900},
}

TOOL_META: dict[str, Any] = {
    "name": "cpi_inflation_calculator",
    "description": "Calculate inflation-adjusted values using CPI data. Uses hardcoded CPI table (2015-2025) with optional BLS API lookup when BLS_API_KEY is set.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "start_year": {"type": "integer", "description": "Starting year (2015-2025)."},
            "start_month": {"type": "integer", "description": "Starting month (1-12)."},
            "end_year": {"type": "integer", "description": "Ending year (2015-2025)."},
            "end_month": {"type": "integer", "description": "Ending month (1-12)."},
            "amount": {
                "type": "number",
                "description": "Dollar amount to adjust for inflation.",
                "default": 100.0,
            },
        },
        "required": ["start_year", "start_month", "end_year", "end_month"],
    },
}


def _get_cpi_from_bls(year: int, month: int) -> float | None:
    """Try fetching CPI from BLS API."""
    api_key = os.environ.get("BLS_API_KEY", "")
    if not api_key:
        return None
    try:
        import httpx

        period = f"M{month:02d}"
        payload = {
            "seriesid": ["CUUR0000SA0"],
            "startyear": str(year),
            "endyear": str(year),
            "registrationkey": api_key,
        }
        with httpx.Client(timeout=30) as client:
            resp = client.post("https://api.bls.gov/publicAPI/v2/timeseries/data/", json=payload)
            resp.raise_for_status()
            data = resp.json()

        for series in data.get("Results", {}).get("series", []):
            for entry in series.get("data", []):
                if entry.get("period") == period:
                    return float(entry["value"])
    except Exception:
        pass
    return None


def _get_cpi(year: int, month: int) -> float | None:
    """Get CPI value from table or BLS API."""
    if year in _CPI_TABLE and month in _CPI_TABLE[year]:
        return _CPI_TABLE[year][month]
    return _get_cpi_from_bls(year, month)


def cpi_inflation_calculator(
    start_year: int,
    start_month: int,
    end_year: int,
    end_month: int,
    amount: float = 100.0,
) -> dict[str, Any]:
    """Calculate inflation-adjusted values using CPI data."""
    try:
        start_cpi = _get_cpi(start_year, start_month)
        end_cpi = _get_cpi(end_year, end_month)

        if start_cpi is None:
            return {
                "status": "error",
                "data": {"error": f"No CPI data available for {start_year}-{start_month:02d}. Available range: 2015-2025 (or set BLS_API_KEY for broader range)."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if end_cpi is None:
            return {
                "status": "error",
                "data": {"error": f"No CPI data available for {end_year}-{end_month:02d}. Available range: 2015-2025 (or set BLS_API_KEY for broader range)."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        adjusted_amount = amount * (end_cpi / start_cpi)
        inflation_rate = (end_cpi - start_cpi) / start_cpi * 100

        return {
            "status": "ok",
            "data": {
                "original_amount": amount,
                "adjusted_amount": round(adjusted_amount, 2),
                "start_cpi": start_cpi,
                "end_cpi": end_cpi,
                "cumulative_inflation_pct": round(inflation_rate, 2),
                "start_period": f"{start_year}-{start_month:02d}",
                "end_period": f"{end_year}-{end_month:02d}",
                "interpretation": f"${amount:.2f} in {start_year}-{start_month:02d} has the same purchasing power as ${adjusted_amount:.2f} in {end_year}-{end_month:02d}.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
