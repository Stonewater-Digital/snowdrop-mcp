---
skill: currency_conversion_calculator
category: fx
description: Convert an amount between two currencies given their USD exchange rates. converted = amount * to_rate / from_rate.
tier: free
inputs: amount
---

# Currency Conversion Calculator

## Description
Convert an amount between two currencies given their USD exchange rates. converted = amount * to_rate / from_rate.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `amount` | `number` | Yes | Amount to convert. |
| `from_rate` | `number` | No | Exchange rate of source currency per USD (e.g. 1.0 for USD, 0.92 for EUR). |
| `to_rate` | `number` | No | Exchange rate of target currency per USD. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "currency_conversion_calculator",
  "arguments": {
    "amount": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "currency_conversion_calculator"`.
