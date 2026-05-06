---
skill: preferred_equity_analyzer
category: reits
description: Calculates preferred equity cash yield, coverage, and call protection metrics.
tier: free
inputs: preferred_equity_amount, coupon_pct, noi_after_debt_service
---

# Preferred Equity Analyzer

## Description
Calculates preferred equity cash yield, coverage, and call protection metrics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `preferred_equity_amount` | `number` | Yes |  |
| `coupon_pct` | `number` | Yes |  |
| `noi_after_debt_service` | `number` | Yes |  |
| `call_protection_years` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "preferred_equity_analyzer",
  "arguments": {
    "preferred_equity_amount": 0,
    "coupon_pct": 0,
    "noi_after_debt_service": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "preferred_equity_analyzer"`.
