---
skill: ebitda_calculator
category: accounting
description: Calculates EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization) by summing net income with non-cash and financing charges.
tier: free
inputs: net_income, interest, taxes, depreciation, amortization
---

# Ebitda Calculator

## Description
Calculates EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization) by summing net income with non-cash and financing charges.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_income` | `number` | Yes | Net income for the period. |
| `interest` | `number` | Yes | Interest expense. |
| `taxes` | `number` | Yes | Tax expense. |
| `depreciation` | `number` | Yes | Depreciation expense. |
| `amortization` | `number` | Yes | Amortization expense. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ebitda_calculator",
  "arguments": {
    "net_income": 0,
    "interest": 0,
    "taxes": 0,
    "depreciation": 0,
    "amortization": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ebitda_calculator"`.
