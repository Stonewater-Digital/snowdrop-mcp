---
skill: estate_tax_estimator
category: tax
description: Estimate federal estate tax at 40% rate on taxable estate exceeding the exemption ($13.61M for 2024) after deductions.
tier: free
inputs: gross_estate
---

# Estate Tax Estimator

## Description
Estimate federal estate tax at 40% rate on taxable estate exceeding the exemption ($13.61M for 2024) after deductions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gross_estate` | `number` | Yes | Gross estate value in USD (total assets at death). |
| `deductions` | `number` | No | Total deductions (marital, charitable, debts, expenses) in USD. |
| `exemption` | `number` | No | Estate tax exemption amount. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "estate_tax_estimator",
  "arguments": {
    "gross_estate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "estate_tax_estimator"`.
