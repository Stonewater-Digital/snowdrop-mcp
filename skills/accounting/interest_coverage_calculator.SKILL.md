---
skill: interest_coverage_calculator
category: accounting
description: Calculates the interest coverage ratio (EBIT / interest expense), measuring a company's ability to meet its interest obligations.
tier: free
inputs: ebit, interest_expense
---

# Interest Coverage Calculator

## Description
Calculates the interest coverage ratio (EBIT / interest expense), measuring a company's ability to meet its interest obligations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ebit` | `number` | Yes | Earnings before interest and taxes. |
| `interest_expense` | `number` | Yes | Total interest expense for the period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "interest_coverage_calculator",
  "arguments": {
    "ebit": 0,
    "interest_expense": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "interest_coverage_calculator"`.
