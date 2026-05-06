---
skill: currency_adjusted_return
category: market_analytics
description: Adjusts local returns for FX moves to measure base-currency performance.
tier: free
inputs: local_returns, fx_rates, base_currency
---

# Currency Adjusted Return

## Description
Adjusts local returns for FX moves to measure base-currency performance.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `local_returns` | `array` | Yes | Local currency returns (decimal). |
| `fx_rates` | `array` | Yes | FX rates as list of {date_idx, rate}. |
| `base_currency` | `string` | Yes | Reporting currency. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "currency_adjusted_return",
  "arguments": {
    "local_returns": [],
    "fx_rates": [],
    "base_currency": "<base_currency>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "currency_adjusted_return"`.
