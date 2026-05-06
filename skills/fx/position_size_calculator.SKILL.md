---
skill: position_size_calculator
category: fx
description: Calculate optimal position size given account balance, risk percentage, stop-loss distance in pips, and pip value.
tier: free
inputs: account_balance
---

# Position Size Calculator

## Description
Calculate optimal position size given account balance, risk percentage, stop-loss distance in pips, and pip value.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `account_balance` | `number` | Yes | Account balance in account currency. |
| `risk_pct` | `number` | No | Risk per trade as a decimal (e.g. 0.02 for 2%). |
| `stop_loss_pips` | `integer` | No | Stop-loss distance in pips. |
| `pip_value` | `number` | No | Value of one pip per standard lot in account currency. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "position_size_calculator",
  "arguments": {
    "account_balance": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "position_size_calculator"`.
