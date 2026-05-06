---
skill: debt_coverage_ratio_calculator
category: real_estate
description: Calculate debt coverage ratio (DSCR = NOI / Annual Debt Service). Lenders typically require DSCR >= 1.20-1.25.
tier: free
inputs: net_operating_income, annual_debt_service
---

# Debt Coverage Ratio Calculator

## Description
Calculate debt coverage ratio (DSCR = NOI / Annual Debt Service). Lenders typically require DSCR >= 1.20-1.25.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_operating_income` | `number` | Yes | Annual net operating income in USD. |
| `annual_debt_service` | `number` | Yes | Total annual debt service (principal + interest payments) in USD. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "debt_coverage_ratio_calculator",
  "arguments": {
    "net_operating_income": 0,
    "annual_debt_service": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "debt_coverage_ratio_calculator"`.
