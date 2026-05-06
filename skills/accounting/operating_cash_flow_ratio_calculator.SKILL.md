---
skill: operating_cash_flow_ratio_calculator
category: accounting
description: Calculates the operating cash flow ratio (OCF / current liabilities), measuring a company's ability to cover short-term obligations with cash from operations.
tier: free
inputs: operating_cash_flow, current_liabilities
---

# Operating Cash Flow Ratio Calculator

## Description
Calculates the operating cash flow ratio (OCF / current liabilities), measuring a company's ability to cover short-term obligations with cash from operations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operating_cash_flow` | `number` | Yes | Cash flow from operations. |
| `current_liabilities` | `number` | Yes | Total current liabilities. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "operating_cash_flow_ratio_calculator",
  "arguments": {
    "operating_cash_flow": 0,
    "current_liabilities": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "operating_cash_flow_ratio_calculator"`.
