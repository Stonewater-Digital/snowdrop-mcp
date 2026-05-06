---
skill: clob_liquidity_score
category: structured_products
description: Computes a composite score from depth-weighted spread, imbalance, and volume decay to quantify CLOB liquidity. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Clob Liquidity Score

## Description
Computes a composite score from depth-weighted spread, imbalance, and volume decay to quantify CLOB liquidity. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "clob_liquidity_score",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "clob_liquidity_score"`.
