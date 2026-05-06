---
skill: occupancy_rate_forecaster
category: real_estate
description: Forecasts occupancy rates for the next 3 periods using simple linear regression on historical data, with optional adjustments for market absorption rate and new supply entering the market.
tier: free
inputs: historical_rates
---

# Occupancy Rate Forecaster

## Description
Forecasts occupancy rates for the next 3 periods using simple linear regression on historical data, with optional adjustments for market absorption rate and new supply entering the market.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `historical_rates` | `array` | Yes | Historical occupancy data points, ordered oldest to newest. |
| `market_absorption_rate` | `number` | No | Expected net absorption rate as decimal (positive = demand > supply). |
| `new_supply_pct` | `number` | No | Percentage of new competing supply entering market as decimal (e.g., 0.03 = 3%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "occupancy_rate_forecaster",
  "arguments": {
    "historical_rates": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "occupancy_rate_forecaster"`.
