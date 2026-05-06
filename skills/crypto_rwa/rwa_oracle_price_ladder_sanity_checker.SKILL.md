---
skill: rwa_oracle_price_ladder_sanity_checker
category: crypto_rwa
description: Validates laddered price levels for order-book fed RWAs remain monotonic.
tier: free
inputs: none
---

# Rwa Oracle Price Ladder Sanity Checker

## Description
Validates laddered price levels for order-book fed RWAs remain monotonic.

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
  "tool": "rwa_oracle_price_ladder_sanity_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_price_ladder_sanity_checker"`.
