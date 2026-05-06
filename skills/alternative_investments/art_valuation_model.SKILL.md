---
skill: art_valuation_model
category: alternative_investments
description: Uses hedonic regression weights calibrated to artist, medium, size, and provenance with comparable sales to estimate value and liquidity.
tier: premium
inputs: artist_score, medium_score, size_sq_in, provenance_score, comparable_sales
---

# Art Valuation Model

## Description
Uses hedonic regression weights calibrated to artist reputation, medium desirability, physical size, and provenance quality, then benchmarks against comparable auction sales to estimate fair value and liquidity. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `artist_score` | `number` | Yes | Artist market reputation score 0–100. |
| `medium_score` | `number` | Yes | Medium desirability score 0–100 (oil > watercolor > print, etc.). |
| `size_sq_in` | `number` | Yes | Canvas or work area in square inches. |
| `provenance_score` | `number` | Yes | Provenance quality score 0–100 (clear title, major collection history). |
| `comparable_sales` | `array` | Yes | List of comparable sale prices (dollars) from recent auctions. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "art_valuation_model",
  "arguments": {
    "artist_score": 82.0,
    "medium_score": 75.0,
    "size_sq_in": 2400,
    "provenance_score": 90.0,
    "comparable_sales": [320000, 415000, 280000, 500000]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "art_valuation_model"`.
