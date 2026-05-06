---
skill: cash_on_cash_return_calculator
category: real_estate
description: Calculate cash-on-cash return: annual pre-tax cash flow divided by total cash invested.
tier: free
inputs: annual_cash_flow, total_cash_invested
---

# Cash On Cash Return Calculator

## Description
Calculate cash-on-cash return: annual pre-tax cash flow divided by total cash invested.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_cash_flow` | `number` | Yes | Annual pre-tax cash flow in USD (after debt service). |
| `total_cash_invested` | `number` | Yes | Total cash invested (down payment + closing costs + rehab) in USD. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cash_on_cash_return_calculator",
  "arguments": {
    "annual_cash_flow": 0,
    "total_cash_invested": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cash_on_cash_return_calculator"`.
