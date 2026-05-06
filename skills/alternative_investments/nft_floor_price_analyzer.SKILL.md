---
skill: nft_floor_price_analyzer
category: alternative_investments
description: Summarizes NFT market data into actionable floor price analytics including depth and wash-trade-adjusted velocity. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Nft Floor Price Analyzer

## Description
Summarizes NFT market data into actionable floor price analytics including depth and wash-trade-adjusted velocity. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "nft_floor_price_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "nft_floor_price_analyzer"`.
