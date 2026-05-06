---
skill: covered_call_analyzer
category: market_analytics
description: Computes payoff, breakeven, and annualized returns for a covered call position.
tier: free
inputs: stock_price, strike, premium, days_to_expiry, cost_basis
---

# Covered Call Analyzer

## Description
Computes payoff, breakeven, and annualized returns for a covered call position.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `stock_price` | `number` | Yes | Current stock price. |
| `strike` | `number` | Yes | Call strike price. |
| `premium` | `number` | Yes | Premium received per share. |
| `days_to_expiry` | `integer` | Yes | Days until option expiration. |
| `cost_basis` | `number` | Yes | Underlying cost basis per share. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "covered_call_analyzer",
  "arguments": {
    "stock_price": 0,
    "strike": 0,
    "premium": 0,
    "days_to_expiry": 0,
    "cost_basis": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "covered_call_analyzer"`.
