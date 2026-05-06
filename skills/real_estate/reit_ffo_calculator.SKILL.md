---
skill: reit_ffo_calculator
category: real_estate
description: Calculates REIT Funds From Operations (FFO) and Adjusted FFO (AFFO) per NAREIT standards. FFO adds back real estate depreciation and amortization to GAAP net income and excludes gains/losses on property sales.
tier: free
inputs: net_income, depreciation, amortization, gains_on_sales, shares_outstanding
---

# Reit Ffo Calculator

## Description
Calculates REIT Funds From Operations (FFO) and Adjusted FFO (AFFO) per NAREIT standards. FFO adds back real estate depreciation and amortization to GAAP net income and excludes gains/losses on property sales.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_income` | `number` | Yes | GAAP net income for the period (dollars). |
| `depreciation` | `number` | Yes | Real estate depreciation added back (dollars). |
| `amortization` | `number` | Yes | Real estate amortization added back (dollars). |
| `gains_on_sales` | `number` | Yes | Net gains on property sales to be excluded (dollars). |
| `shares_outstanding` | `number` | Yes | Weighted-average diluted shares outstanding. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "reit_ffo_calculator",
  "arguments": {
    "net_income": 0,
    "depreciation": 0,
    "amortization": 0,
    "gains_on_sales": 0,
    "shares_outstanding": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "reit_ffo_calculator"`.
