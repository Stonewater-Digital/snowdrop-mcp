---
skill: multi_currency_consolidator
category: i18n
description: Converts positions into a base currency with exposure diagnostics.
tier: free
inputs: positions, fx_rates
---

# Multi Currency Consolidator

## Description
Converts positions into a base currency with exposure diagnostics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes |  |
| `fx_rates` | `object` | Yes |  |
| `base_currency` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "multi_currency_consolidator",
  "arguments": {
    "positions": [],
    "fx_rates": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "multi_currency_consolidator"`.
