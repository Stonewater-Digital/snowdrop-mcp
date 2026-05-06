---
skill: forward_rate_calculator
category: fx
description: Calculate forward exchange rate using covered interest rate parity: forward = spot * (1 + domestic_rate * days/360) / (1 + foreign_rate * days/360).
tier: free
inputs: spot_rate, domestic_rate, foreign_rate
---

# Forward Rate Calculator

## Description
Calculate forward exchange rate using covered interest rate parity: forward = spot * (1 + domestic_rate * days/360) / (1 + foreign_rate * days/360).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spot_rate` | `number` | Yes | Current spot exchange rate. |
| `domestic_rate` | `number` | Yes | Domestic (quote currency) annualized interest rate as a decimal. |
| `foreign_rate` | `number` | Yes | Foreign (base currency) annualized interest rate as a decimal. |
| `days` | `integer` | No | Forward contract period in days. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "forward_rate_calculator",
  "arguments": {
    "spot_rate": 0,
    "domestic_rate": 0,
    "foreign_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "forward_rate_calculator"`.
