---
skill: exchange_rate_fetcher
category: public_data
description: Fetch currency exchange rate between two currencies using a free API. Returns rate and inverse.
tier: free
inputs: none
---

# Exchange Rate Fetcher

## Description
Fetch currency exchange rate between two currencies using a free API. Returns rate and inverse.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `base_currency` | `string` | No | Base currency ISO 4217 code (e.g., 'USD'). |
| `target_currency` | `string` | No | Target currency ISO 4217 code (e.g., 'EUR'). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "exchange_rate_fetcher",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "exchange_rate_fetcher"`.
