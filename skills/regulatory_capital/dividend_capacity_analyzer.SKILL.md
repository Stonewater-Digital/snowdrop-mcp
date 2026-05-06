---
skill: dividend_capacity_analyzer
category: regulatory_capital
description: Determines MDA and dividend restrictions relative to combined capital buffer requirements.
tier: free
inputs: cet1_ratio_pct, combined_buffer_requirement_pct, distributable_profits, risk_weighted_assets
---

# Dividend Capacity Analyzer

## Description
Determines MDA and dividend restrictions relative to combined capital buffer requirements.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cet1_ratio_pct` | `number` | Yes | Current CET1 ratio. |
| `combined_buffer_requirement_pct` | `number` | Yes | Capital conservation + CCyB + G-SIB buffer. |
| `distributable_profits` | `number` | Yes | Current year distributable profits. |
| `risk_weighted_assets` | `number` | Yes | RWA amount. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dividend_capacity_analyzer",
  "arguments": {
    "cet1_ratio_pct": 0,
    "combined_buffer_requirement_pct": 0,
    "distributable_profits": 0,
    "risk_weighted_assets": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dividend_capacity_analyzer"`.
