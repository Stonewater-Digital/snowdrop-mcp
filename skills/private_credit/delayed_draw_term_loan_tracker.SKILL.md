---
skill: delayed_draw_term_loan_tracker
category: private_credit
description: Calculates drawn/undrawn balances, fees, and blended costs for DDTLs.
tier: free
inputs: total_commitment, draws, commitment_fee_bps, drawn_spread_bps, draw_period_end
---

# Delayed Draw Term Loan Tracker

## Description
Calculates drawn/undrawn balances, fees, and blended costs for DDTLs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_commitment` | `number` | Yes |  |
| `draws` | `array` | Yes |  |
| `commitment_fee_bps` | `integer` | Yes |  |
| `drawn_spread_bps` | `integer` | Yes |  |
| `draw_period_end` | `string` | Yes |  |
| `availability_conditions` | `array` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "delayed_draw_term_loan_tracker",
  "arguments": {
    "total_commitment": 0,
    "draws": [],
    "commitment_fee_bps": 0,
    "drawn_spread_bps": 0,
    "draw_period_end": "<draw_period_end>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "delayed_draw_term_loan_tracker"`.
