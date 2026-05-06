---
skill: sector_etf_comparator
category: market_analytics
description: Ranks sector ETFs by performance metrics over a labelled period.
tier: free
inputs: sector_returns, period_label
---

# Sector Etf Comparator

## Description
Ranks sector ETFs by performance metrics over a labelled period.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sector_returns` | `object` | Yes | Mapping of ETF ticker to return series. |
| `period_label` | `string` | Yes | Label for reporting period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sector_etf_comparator",
  "arguments": {
    "sector_returns": {},
    "period_label": "<period_label>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sector_etf_comparator"`.
