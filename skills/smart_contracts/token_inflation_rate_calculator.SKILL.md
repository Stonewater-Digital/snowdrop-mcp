---
skill: token_inflation_rate_calculator
category: smart_contracts
description: Transforms token emission inputs into annualized inflation metrics.
tier: free
inputs: current_supply, new_tokens_per_period, periods_per_year
---

# Token Inflation Rate Calculator

## Description
Transforms token emission inputs into annualized inflation metrics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_supply` | `number` | Yes | Circulating supply |
| `new_tokens_per_period` | `number` | Yes | Tokens emitted each period |
| `periods_per_year` | `number` | Yes | Number of emission periods in a year |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_inflation_rate_calculator",
  "arguments": {
    "current_supply": 0,
    "new_tokens_per_period": 0,
    "periods_per_year": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_inflation_rate_calculator"`.
