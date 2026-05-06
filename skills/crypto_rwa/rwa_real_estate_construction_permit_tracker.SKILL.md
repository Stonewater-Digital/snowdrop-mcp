---
skill: rwa_real_estate_construction_permit_tracker
category: crypto_rwa
description: Aligns construction draw schedules with permit milestones to gate unlocks.
tier: free
inputs: payload
---

# Rwa Real Estate Construction Permit Tracker

## Description
Aligns construction draw schedules with permit milestones to gate unlocks.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_real_estate_construction_permit_tracker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_construction_permit_tracker"`.
