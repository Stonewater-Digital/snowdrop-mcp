---
skill: real_rate_calculator
category: quant
description: Computes ex-ante and ex-post real rates using Fisher relations.
tier: free
inputs: nominal_yield_pct, inflation_expectation_pct
---

# Real Rate Calculator

## Description
Computes ex-ante and ex-post real rates using Fisher relations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `nominal_yield_pct` | `number` | Yes |  |
| `inflation_expectation_pct` | `number` | Yes |  |
| `realized_inflation_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "real_rate_calculator",
  "arguments": {
    "nominal_yield_pct": 0,
    "inflation_expectation_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "real_rate_calculator"`.
