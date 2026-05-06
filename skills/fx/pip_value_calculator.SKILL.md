---
skill: pip_value_calculator
category: fx
description: Calculate the monetary value of a single pip for a given currency pair and lot size. Handles JPY pairs (pip = 0.01) and standard pairs (pip = 0.0001).
tier: free
inputs: pair
---

# Pip Value Calculator

## Description
Calculate the monetary value of a single pip for a given currency pair and lot size. Handles JPY pairs (pip = 0.01) and standard pairs (pip = 0.0001).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pair` | `string` | Yes | Currency pair (e.g. 'EUR/USD', 'USD/JPY'). |
| `lot_size` | `number` | No | Position size in units of base currency. |
| `account_currency` | `string` | No | Account denomination currency. |
| `exchange_rate` | `number` | No | Current exchange rate of the pair (quote currency per base currency). Used to convert pip value to account currency if needed. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "pip_value_calculator",
  "arguments": {
    "pair": "<pair>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pip_value_calculator"`.
