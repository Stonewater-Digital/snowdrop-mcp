---
skill: big_mac_index_calculator
category: public_data
description: Calculate the Big Mac Index to assess whether a currency is over- or under-valued relative to the US dollar based on purchasing power parity.
tier: free
inputs: local_price, local_currency, exchange_rate
---

# Big Mac Index Calculator

## Description
Calculate the Big Mac Index to assess whether a currency is over- or under-valued relative to the US dollar based on purchasing power parity.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `local_price` | `number` | Yes | Price of a Big Mac in local currency. |
| `local_currency` | `string` | Yes | ISO 4217 currency code (e.g., 'GBP', 'JPY', 'EUR'). |
| `usd_price` | `number` | No | Price of a Big Mac in USD. |
| `exchange_rate` | `number` | Yes | Actual market exchange rate (local currency per 1 USD). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "big_mac_index_calculator",
  "arguments": {
    "local_price": 0,
    "local_currency": "<local_currency>",
    "exchange_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "big_mac_index_calculator"`.
