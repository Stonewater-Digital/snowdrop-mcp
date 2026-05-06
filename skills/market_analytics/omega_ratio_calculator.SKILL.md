---
skill: omega_ratio_calculator
category: market_analytics
description: Computes Omega = sum(max(r-threshold,0)) / sum(max(threshold-r,0)).
tier: free
inputs: returns, threshold_return
---

# Omega Ratio Calculator

## Description
Computes Omega = sum(max(r-threshold,0)) / sum(max(threshold-r,0)).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | Return series. |
| `threshold_return` | `number` | Yes | Target or hurdle return (decimal). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "omega_ratio_calculator",
  "arguments": {
    "returns": [],
    "threshold_return": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "omega_ratio_calculator"`.
