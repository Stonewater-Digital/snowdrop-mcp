---
skill: market_value_calculator
category: middle_office
description: Converts multi-currency positions to a base currency and aggregates exposure.
tier: free
inputs: positions, fx_rates, base_currency
---

# Market Value Calculator

## Description
Converts multi-currency positions to a base currency and aggregates exposure.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes |  |
| `fx_rates` | `object` | Yes |  |
| `base_currency` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "market_value_calculator",
  "arguments": {
    "positions": [],
    "fx_rates": {},
    "base_currency": "<base_currency>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "market_value_calculator"`.
