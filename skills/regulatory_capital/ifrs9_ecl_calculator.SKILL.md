---
skill: ifrs9_ecl_calculator
category: regulatory_capital
description: Computes 12-month and lifetime ECL discounted at the effective interest rate per IFRS 9.
tier: free
inputs: pd_term_structure, lgd_pct, ead, discount_rate_pct, stage
---

# Ifrs9 Ecl Calculator

## Description
Computes 12-month and lifetime ECL discounted at the effective interest rate per IFRS 9.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pd_term_structure` | `array` | Yes | List of PD points with tenor in years (cumulative PD). |
| `lgd_pct` | `number` | Yes | Loss given default percentage. |
| `ead` | `number` | Yes | Exposure at default. |
| `discount_rate_pct` | `number` | Yes | Effective interest rate used for discounting. |
| `stage` | `integer` | Yes | IFRS 9 stage (1,2,3). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ifrs9_ecl_calculator",
  "arguments": {
    "pd_term_structure": [],
    "lgd_pct": 0,
    "ead": 0,
    "discount_rate_pct": 0,
    "stage": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ifrs9_ecl_calculator"`.
