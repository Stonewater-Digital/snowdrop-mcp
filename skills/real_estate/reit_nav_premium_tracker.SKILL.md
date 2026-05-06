---
skill: reit_nav_premium_tracker
category: real_estate
description: Tracks the premium or discount of a REIT's market price relative to Net Asset Value (NAV) per share. Computes a z-score against historical premiums (when provided) and signals overvalued, undervalued, or fair value.
tier: free
inputs: market_price, nav_per_share
---

# Reit Nav Premium Tracker

## Description
Tracks the premium or discount of a REIT's market price relative to Net Asset Value (NAV) per share. Computes a z-score against historical premiums (when provided) and signals overvalued, undervalued, or fair value.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `market_price` | `number` | Yes | Current market price per share (dollars). |
| `nav_per_share` | `number` | Yes | Estimated NAV per share (dollars). |
| `historical_premiums` | `array` | No | Historical premium percentages (e.g., [5.2, -3.1, 8.0]) for z-score context. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "reit_nav_premium_tracker",
  "arguments": {
    "market_price": 0,
    "nav_per_share": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "reit_nav_premium_tracker"`.
