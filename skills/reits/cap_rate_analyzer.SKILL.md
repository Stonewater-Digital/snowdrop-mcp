---
skill: cap_rate_analyzer
category: reits
description: Computes actual cap rate and implied value relative to market cap rates.
tier: free
inputs: net_operating_income, asset_value, market_cap_rate_pct
---

# Cap Rate Analyzer

## Description
Computes actual cap rate and implied value relative to market cap rates.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_operating_income` | `number` | Yes |  |
| `asset_value` | `number` | Yes |  |
| `market_cap_rate_pct` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cap_rate_analyzer",
  "arguments": {
    "net_operating_income": 0,
    "asset_value": 0,
    "market_cap_rate_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cap_rate_analyzer"`.
