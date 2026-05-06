---
skill: rwa_oracle_shipping_rate_feed_watcher
category: crypto_rwa
description: Checks Baltic Dry and Freightos prints versus oracle shipping feeds for divergence.
tier: free
inputs: none
---

# Rwa Oracle Shipping Rate Feed Watcher

## Description
Checks Baltic Dry and Freightos prints versus oracle shipping feeds for divergence.

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
  "tool": "rwa_oracle_shipping_rate_feed_watcher",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_shipping_rate_feed_watcher"`.
