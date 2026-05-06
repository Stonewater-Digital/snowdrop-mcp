---
skill: freight_rate_analyzer
category: commodities
description: Evaluates shipping freight index momentum, route-level rate dispersion, and market tightness signals for dry bulk, tanker, or container markets.
tier: free
inputs: index_history, route_rates
---

# Freight Rate Analyzer

## Description
Evaluates shipping freight index momentum, route-level rate dispersion, and market tightness signals for dry bulk, tanker, or container markets.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `index_history` | `array` | Yes | Freight index time series (e.g. Baltic Dry Index), oldest to newest. Min 2 points. |
| `route_rates` | `array` | Yes | Current rate observations by route. |
| `tightness_threshold_pct` | `number` | No | % gain from start of series to flag 'tight' market. Default 20%. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "freight_rate_analyzer",
  "arguments": {
    "index_history": [],
    "route_rates": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "freight_rate_analyzer"`.
