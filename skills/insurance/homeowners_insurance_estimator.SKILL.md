---
skill: homeowners_insurance_estimator
category: insurance
description: Estimate homeowners insurance annual premium based on home value, contents value, and deductible. Range: 0.3%-0.5% of home value adjusted by deductible.
tier: free
inputs: home_value
---

# Homeowners Insurance Estimator

## Description
Estimate homeowners insurance annual premium based on home value, contents value, and deductible. Range: 0.3%-0.5% of home value adjusted by deductible.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `home_value` | `number` | Yes | Estimated home replacement value. |
| `contents_value` | `number` | No | Estimated contents/personal property value (default 0). |
| `deductible` | `number` | No | Policy deductible (default 1000). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "homeowners_insurance_estimator",
  "arguments": {
    "home_value": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "homeowners_insurance_estimator"`.
