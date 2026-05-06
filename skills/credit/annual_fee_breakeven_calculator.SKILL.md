---
skill: annual_fee_breakeven_calculator
category: credit
description: Calculate how much you need to spend to break even on a credit card's annual fee through rewards earnings.
tier: free
inputs: annual_fee, rewards_rate_pct, avg_monthly_spend
---

# Annual Fee Breakeven Calculator

## Description
Calculate how much you need to spend to break even on a credit card's annual fee through rewards earnings.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_fee` | `number` | Yes | Card annual fee in dollars. |
| `rewards_rate_pct` | `number` | Yes | Rewards rate as percentage (e.g., 2.0 for 2%). |
| `avg_monthly_spend` | `number` | Yes | Average monthly spending on the card. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "annual_fee_breakeven_calculator",
  "arguments": {
    "annual_fee": 0,
    "rewards_rate_pct": 0,
    "avg_monthly_spend": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "annual_fee_breakeven_calculator"`.
