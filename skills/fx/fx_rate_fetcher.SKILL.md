---
skill: fx_rate_fetcher
category: fx
description: Retrieves spot FX quotes and inverse rates via ExchangeRate-API.
tier: free
inputs: none
---

# Fx Rate Fetcher

## Description
Retrieves spot FX quotes and inverse rates via ExchangeRate-API.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `base_currency` | `string` | No |  |
| `target_currencies` | `array` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fx_rate_fetcher",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fx_rate_fetcher"`.
