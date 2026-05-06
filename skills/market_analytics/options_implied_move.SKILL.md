---
skill: options_implied_move
category: market_analytics
description: Converts ATM straddle pricing into implied move, range, and annualized IV approximation.
tier: free
inputs: atm_straddle_price, stock_price, days_to_expiry
---

# Options Implied Move

## Description
Converts ATM straddle pricing into implied move, range, and annualized IV approximation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `atm_straddle_price` | `number` | Yes | Cost of ATM straddle (call+put). |
| `stock_price` | `number` | Yes | Underlying price. |
| `days_to_expiry` | `integer` | Yes | Days until the option expires. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "options_implied_move",
  "arguments": {
    "atm_straddle_price": 0,
    "stock_price": 0,
    "days_to_expiry": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "options_implied_move"`.
