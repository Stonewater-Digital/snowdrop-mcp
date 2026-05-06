---
skill: cds_spread_calculator
category: credit_default_swaps
description: Estimates CDS par spread and expected loss using default probabilities.
tier: free
inputs: notional, default_probability_pct, recovery_rate_pct, maturity_years
---

# Cds Spread Calculator

## Description
Estimates CDS par spread and expected loss using default probabilities.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `notional` | `number` | Yes |  |
| `default_probability_pct` | `number` | Yes |  |
| `recovery_rate_pct` | `number` | Yes |  |
| `maturity_years` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_spread_calculator",
  "arguments": {
    "notional": 0,
    "default_probability_pct": 0,
    "recovery_rate_pct": 0,
    "maturity_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_spread_calculator"`.
