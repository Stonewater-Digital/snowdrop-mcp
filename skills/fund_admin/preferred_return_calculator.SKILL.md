---
skill: preferred_return_calculator
category: fund_admin
description: Calculates accrued preferred return on LP capital with configurable compounding frequency. Supports annual, quarterly, monthly, and daily compounding.
tier: premium
inputs: capital_balance, pref_rate_pct, period_years, compounding
---

# Preferred Return Calculator

## Description
Calculates accrued preferred return on LP capital with configurable compounding frequency. Supports annual, quarterly, monthly, and daily compounding. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| capital_balance | number | Yes | LP capital balance on which the preferred return accrues (USD) |
| pref_rate_pct | number | Yes | Annual preferred return rate (hurdle rate, e.g. 8.0 for 8%) |
| period_years | number | Yes | Accrual period in years (e.g. 0.25 for one quarter, 3.5 for three and a half years) |
| compounding | string | No | Compounding frequency: "annual", "quarterly", "monthly", or "daily" (default: "quarterly") |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "preferred_return_calculator",
  "arguments": {
    "capital_balance": 25000000,
    "pref_rate_pct": 8.0,
    "period_years": 4.5,
    "compounding": "quarterly"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "preferred_return_calculator"`.
