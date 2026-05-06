---
skill: var_calculator
category: middle_office
description: Computes one-day VaR using historical percentile and parametric methods.
tier: free
inputs: returns, portfolio_value
---

# Var Calculator

## Description
Computes one-day VaR using historical percentile and parametric methods.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes |  |
| `confidence_pct` | `number` | No |  |
| `portfolio_value` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "var_calculator",
  "arguments": {
    "returns": [],
    "portfolio_value": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "var_calculator"`.
