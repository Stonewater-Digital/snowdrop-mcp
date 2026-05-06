---
skill: asset_swap_spread
category: structured_products
description: Derives the par asset swap spread and constant Z-spread using swap discount factors and root-finding. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Asset Swap Spread

## Description
Derives the par asset swap spread and constant Z-spread using swap discount factors and root-finding. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "asset_swap_spread",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "asset_swap_spread"`.
