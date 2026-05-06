---
skill: free_cash_flow_calculator
category: accounting
description: Calculates free cash flow (FCF = operating cash flow - capital expenditures), measuring cash available for distribution to investors.
tier: free
inputs: operating_cash_flow, capital_expenditures
---

# Free Cash Flow Calculator

## Description
Calculates free cash flow (FCF = operating cash flow - capital expenditures), measuring cash available for distribution to investors.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operating_cash_flow` | `number` | Yes | Cash flow from operations. |
| `capital_expenditures` | `number` | Yes | Capital expenditures (positive number). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "free_cash_flow_calculator",
  "arguments": {
    "operating_cash_flow": 0,
    "capital_expenditures": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "free_cash_flow_calculator"`.
