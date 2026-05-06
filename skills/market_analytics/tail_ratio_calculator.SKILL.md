---
skill: tail_ratio_calculator
category: market_analytics
description: Calculates right-tail/left-tail ratio plus skewness and kurtosis for fat-tail detection.
tier: free
inputs: returns, percentile
---

# Tail Ratio Calculator

## Description
Calculates right-tail/left-tail ratio plus skewness and kurtosis for fat-tail detection.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | Return series. |
| `percentile` | `number` | Yes | Tail percentile (e.g., 5 for 5%%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tail_ratio_calculator",
  "arguments": {
    "returns": [],
    "percentile": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tail_ratio_calculator"`.
