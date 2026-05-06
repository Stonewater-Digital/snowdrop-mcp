---
skill: franchise_onboarder
category: watering_hole
description: Checks franchise safety gates and returns royalty terms.
tier: free
inputs: operator_id, security_audit_score, has_bouncer
---

# Franchise Onboarder

## Description
Checks franchise safety gates and returns royalty terms.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operator_id` | `string` | Yes |  |
| `security_audit_score` | `number` | Yes |  |
| `has_bouncer` | `boolean` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "franchise_onboarder",
  "arguments": {
    "operator_id": "<operator_id>",
    "security_audit_score": 0,
    "has_bouncer": false
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "franchise_onboarder"`.
