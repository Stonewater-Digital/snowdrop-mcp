---
skill: tax_loss_harvesting_calculator
category: personal_finance
description: Aggregates available capital losses to offset realized gains, estimates tax savings (federal + state), and flags 30-day wash sale blackout periods.
tier: free
inputs: realized_gains, unrealized_losses, tax_bracket, state_rate
---

# Tax Loss Harvesting Calculator

## Description
Aggregates available capital losses to offset realized gains, estimates tax savings (federal + state), and flags 30-day wash sale blackout periods.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `realized_gains` | `number` | Yes | Net realized capital gains so far this year. |
| `unrealized_losses` | `array` | Yes | List of holdings with loss amounts and holding_period days. |
| `tax_bracket` | `number` | Yes | Marginal federal capital gains rate as decimal. |
| `state_rate` | `number` | Yes | State tax rate applicable to capital gains. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tax_loss_harvesting_calculator",
  "arguments": {
    "realized_gains": 0,
    "unrealized_losses": [],
    "tax_bracket": 0,
    "state_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tax_loss_harvesting_calculator"`.
