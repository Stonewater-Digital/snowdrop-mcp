---
skill: construction_draw_validator
category: real_estate
description: Validates a construction loan draw request by verifying that receipts sum to the requested amount, the milestone exists and has sufficient remaining budget, and completion percentage is consistent. Returns approval status, discrepancy list, and remaining milestone budget.
tier: free
inputs: draw_request, milestones
---

# Construction Draw Validator

## Description
Validates a construction loan draw request by verifying that receipts sum to the requested amount, the milestone exists and has sufficient remaining budget, and completion percentage is consistent. Returns approval status, discrepancy list, and remaining milestone budget.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `draw_request` | `object` | Yes | Draw request submitted by the contractor. |
| `milestones` | `array` | Yes | Master milestone schedule from the construction contract. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "construction_draw_validator",
  "arguments": {
    "draw_request": {},
    "milestones": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "construction_draw_validator"`.
