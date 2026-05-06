---
skill: property_tax_estimator
category: tax
description: Estimate annual and monthly property tax from assessed value, mill rate, and optional homestead exemption.
tier: free
inputs: assessed_value, mill_rate
---

# Property Tax Estimator

## Description
Estimate annual and monthly property tax from assessed value, mill rate, and optional homestead exemption.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `assessed_value` | `number` | Yes | Assessed property value in USD. |
| `mill_rate` | `number` | Yes | Mill rate (tax per $1,000 of assessed value). E.g. 25 means $25 per $1,000. |
| `homestead_exemption` | `number` | No | Homestead exemption amount in USD. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "property_tax_estimator",
  "arguments": {
    "assessed_value": 0,
    "mill_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "property_tax_estimator"`.
