---
skill: fx_profit_loss_calculator
category: fx
description: Calculate profit/loss for a forex trade given entry price, exit price, lot size, and direction (long/short). Computes P&L in pips and currency.
tier: free
inputs: entry_price, exit_price
---

# Fx Profit Loss Calculator

## Description
Calculate profit/loss for a forex trade given entry price, exit price, lot size, and direction (long/short). Computes P&L in pips and currency.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `entry_price` | `number` | Yes | Trade entry price. |
| `exit_price` | `number` | Yes | Trade exit price. |
| `lot_size` | `number` | No | Position size in units of base currency. |
| `direction` | `string` | No | Trade direction: 'long' or 'short'. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fx_profit_loss_calculator",
  "arguments": {
    "entry_price": 0,
    "exit_price": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fx_profit_loss_calculator"`.
