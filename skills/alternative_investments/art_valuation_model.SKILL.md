---
skill: art_valuation_model
category: alternative_investments
description: Uses hedonic regression weights calibrated to artist, medium, size, and provenance with comparable sales to estimate value and liquidity. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Art Valuation Model

## Description
Uses hedonic regression weights calibrated to artist, medium, size, and provenance with comparable sales to estimate value and liquidity. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "art_valuation_model",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "art_valuation_model"`.
