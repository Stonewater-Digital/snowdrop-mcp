---
skill: price_feed_aggregator
category: crypto
description: Fetches CoinGecko and Kraken prices then returns the median.
tier: free
inputs: asset_symbol
---

# Price Feed Aggregator

## Description
Fetches CoinGecko and Kraken prices then returns the median.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset_symbol` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "price_feed_aggregator",
  "arguments": {
    "asset_symbol": "<asset_symbol>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "price_feed_aggregator"`.
