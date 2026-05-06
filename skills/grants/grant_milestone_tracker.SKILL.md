---
skill: grant_milestone_tracker
category: grants
description: Summarizes milestone completion, disbursements, and deadlines for grants.
tier: free
inputs: grant_id, milestones
---

# Grant Milestone Tracker

## Description
Summarizes milestone completion, disbursements, and deadlines for grants.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `grant_id` | `string` | Yes |  |
| `milestones` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "grant_milestone_tracker",
  "arguments": {
    "grant_id": "<grant_id>",
    "milestones": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "grant_milestone_tracker"`.
