---
skill: vendor_cost_comparator
category: vendors
description: Computes daily/monthly spend per provider and ranks by cost-effectiveness.
tier: free
inputs: task_profile, providers
---

# Vendor Cost Comparator

## Description
Computes daily/monthly spend per provider and ranks by cost-effectiveness.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_profile` | `object` | Yes |  |
| `providers` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "vendor_cost_comparator",
  "arguments": {
    "task_profile": {},
    "providers": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vendor_cost_comparator"`.
