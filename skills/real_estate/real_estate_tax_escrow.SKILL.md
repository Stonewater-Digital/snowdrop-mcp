---
skill: real_estate_tax_escrow
category: real_estate
description: Calculates monthly escrow reserve requirements for property taxes and insurance. Uses the millage rate system (mills per $1,000 of assessed value).
tier: free
inputs: assessed_value, tax_rate
---

# Real Estate Tax Escrow

## Description
Calculates monthly escrow reserve requirements for property taxes and insurance. Uses the millage rate system (mills per $1,000 of assessed value). Outputs monthly escrow, annual tax, and combined annual total.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `assessed_value` | `number` | Yes | Assessed property value for tax purposes (dollars). |
| `tax_rate` | `number` | Yes | Property tax rate in mills (e.g., 25 = $25 per $1,000 assessed value). |
| `annual_insurance` | `number` | No | Annual property insurance premium (dollars, optional). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "real_estate_tax_escrow",
  "arguments": {
    "assessed_value": 0,
    "tax_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "real_estate_tax_escrow"`.
