---
skill: seasonal_pattern_analyzer
category: commodities
description: Aggregates historical commodity prices by calendar month to estimate seasonal factors, identify peak and trough months, and compute seasonal amplitude.
tier: free
inputs: monthly_prices
---

# Seasonal Pattern Analyzer

## Description
Aggregates historical commodity prices by calendar month to estimate seasonal factors, identify peak and trough months, and compute seasonal amplitude.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `monthly_prices` | `array` | Yes | Historical price observations with month labels. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "seasonal_pattern_analyzer",
  "arguments": {
    "monthly_prices": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "seasonal_pattern_analyzer"`.
