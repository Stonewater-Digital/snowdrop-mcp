---
skill: gold_price_fetcher
category: public_data
description: Fetch the current gold price per troy ounce in USD. Tries metals.dev API or returns recent reference price.
tier: free
inputs: none
---

# Gold Price Fetcher

## Description
Fetch the current gold price per troy ounce in USD. Tries metals.dev API or returns recent reference price.

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
  "tool": "gold_price_fetcher",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gold_price_fetcher"`.
