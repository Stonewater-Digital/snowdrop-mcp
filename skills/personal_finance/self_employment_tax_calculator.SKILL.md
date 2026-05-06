---
skill: self_employment_tax_calculator
category: personal_finance
description: Computes Social Security and Medicare self-employment tax components, including the deductible half and additional Medicare surtax.
tier: free
inputs: net_self_employment_income
---

# Self Employment Tax Calculator

## Description
Computes Social Security and Medicare self-employment tax components, including the deductible half and additional Medicare surtax.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_self_employment_income` | `number` | Yes | Schedule C or partnership net earnings subject to SE tax. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "self_employment_tax_calculator",
  "arguments": {
    "net_self_employment_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "self_employment_tax_calculator"`.
