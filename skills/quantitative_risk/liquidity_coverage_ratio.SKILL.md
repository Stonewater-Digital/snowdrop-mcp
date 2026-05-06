---
skill: liquidity_coverage_ratio
category: quantitative_risk
description: Basel III LCR computation with supervisory caps on Level 2 assets and haircut adjustments.
tier: free
inputs: hqlas, net_cash_outflows
---

# Liquidity Coverage Ratio

## Description
Basel III LCR computation with supervisory caps on Level 2 assets and haircut adjustments.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `hqlas` | `object` | Yes | High quality liquid asset balances by level (base currency). |
| `haircuts` | `object` | No | Haircut percentages per LCR rules (0-100). |
| `net_cash_outflows` | `number` | Yes | 30-day stressed net cash outflows as per Basel formula. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "liquidity_coverage_ratio",
  "arguments": {
    "hqlas": {},
    "net_cash_outflows": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "liquidity_coverage_ratio"`.
