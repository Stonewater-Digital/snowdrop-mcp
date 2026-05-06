---
skill: price_feed_aggregator
category: crypto
description: Fetches CoinGecko and Kraken prices then returns the median.
tier: free
inputs: none
---

# Price Feed Aggregator

## Description
Fetches CoinGecko and Kraken prices then returns the median.

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "price_feed_aggregator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "price_feed_aggregator"`.
