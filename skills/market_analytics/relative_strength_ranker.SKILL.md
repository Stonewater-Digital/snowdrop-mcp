---
skill: relative_strength_ranker
category: market_analytics
description: Computes total returns over multiple lookbacks and ranks assets by composite score.
tier: free
inputs: assets, lookback_periods
---

# Relative Strength Ranker

## Description
Computes total returns over multiple lookbacks and ranks assets by composite score.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `assets` | `object` | Yes | Mapping of asset name to price series. |
| `lookback_periods` | `array` | Yes | List of lookback windows (in bars). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "relative_strength_ranker",
  "arguments": {
    "assets": {},
    "lookback_periods": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "relative_strength_ranker"`.
