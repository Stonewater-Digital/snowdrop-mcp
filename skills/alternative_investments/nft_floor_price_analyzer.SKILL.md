---
skill: nft_floor_price_analyzer
category: alternative_investments
description: Summarizes NFT market data into actionable floor price analytics including depth and wash-trade-adjusted velocity. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: recent_sales, listings, holder_distribution, wash_trade_ratio
---

# NFT Floor Price Analyzer

## Description
Summarizes NFT collection market data into actionable floor price analytics including listing depth, wash-trade-adjusted velocity, and holder concentration metrics. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `recent_sales` | `array` | Yes | List of recent sale prices in ETH or USD (newest first). |
| `listings` | `array` | Yes | List of current active listing prices across the collection. |
| `holder_distribution` | `array` | Yes | List of token counts per unique holder (concentration data). |
| `wash_trade_ratio` | `number` | Yes | Estimated wash trading fraction as a decimal (e.g. 0.15 for 15%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "nft_floor_price_analyzer",
  "arguments": {
    "recent_sales": [1.2, 1.5, 1.1, 1.8, 1.3],
    "listings": [1.1, 1.2, 1.4, 1.6, 2.0, 2.5],
    "holder_distribution": [5, 3, 1, 1, 12, 2, 8, 1],
    "wash_trade_ratio": 0.12
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "nft_floor_price_analyzer"`.
