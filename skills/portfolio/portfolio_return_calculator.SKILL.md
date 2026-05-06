---
skill: portfolio_return_calculator
category: portfolio
description: Calculates the weighted portfolio return as the sum of weight * return for each asset.
tier: free
inputs: weights, returns
---

# Portfolio Return Calculator

## Description
Calculates the weighted portfolio return as the sum of weight * return for each asset.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `weights` | `array` | Yes | List of asset weights (should sum to 1). |
| `returns` | `array` | Yes | List of asset returns (same length as weights). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "portfolio_return_calculator",
  "arguments": {
    "weights": [],
    "returns": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portfolio_return_calculator"`.
