---
skill: credit_facility_utilization_monitor
category: private_credit
description: Aggregates revolver/DDTL/term loan utilization and identifies spread tiers.
tier: free
inputs: facilities
---

# Credit Facility Utilization Monitor

## Description
Aggregates revolver/DDTL/term loan utilization and identifies spread tiers.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `facilities` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_facility_utilization_monitor",
  "arguments": {
    "facilities": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_facility_utilization_monitor"`.
