---
skill: distressed_debt_screener
category: private_credit
description: Flags distressed signals using price, spread, PD, and coverage metrics.
tier: free
inputs: price_pct_of_par, spread_bps, prob_default_pct, interest_coverage
---

# Distressed Debt Screener

## Description
Flags distressed signals using price, spread, PD, and coverage metrics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `price_pct_of_par` | `number` | Yes |  |
| `spread_bps` | `number` | Yes |  |
| `prob_default_pct` | `number` | Yes |  |
| `interest_coverage` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "distressed_debt_screener",
  "arguments": {
    "price_pct_of_par": 0,
    "spread_bps": 0,
    "prob_default_pct": 0,
    "interest_coverage": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "distressed_debt_screener"`.
