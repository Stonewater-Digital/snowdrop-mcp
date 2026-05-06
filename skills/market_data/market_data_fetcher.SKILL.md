---
skill: market_data_fetcher
category: market_data
description: Pulls CoinGecko quotes and 24h change metrics.
tier: free
inputs: assets
---

# Market Data Fetcher

## Description
Pulls CoinGecko quotes and 24h change metrics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `assets` | `array` | Yes |  |
| `vs_currency` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "market_data_fetcher",
  "arguments": {
    "assets": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "market_data_fetcher"`.
