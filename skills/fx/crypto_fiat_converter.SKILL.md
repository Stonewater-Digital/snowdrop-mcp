---
skill: crypto_fiat_converter
category: fx
description: Uses USD hub conversions (pending Thunder approval for transfers).
tier: free
inputs: amount, from_currency, to_currency
---

# Crypto Fiat Converter

## Description
Uses USD hub conversions (pending Thunder approval for transfers).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `amount` | `number` | Yes |  |
| `from_currency` | `string` | Yes |  |
| `to_currency` | `string` | Yes |  |
| `prices` | `object` | No | Optional override mapping currency -> USD rate or dict with usd key. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "crypto_fiat_converter",
  "arguments": {
    "amount": 0,
    "from_currency": "<from_currency>",
    "to_currency": "<to_currency>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "crypto_fiat_converter"`.
