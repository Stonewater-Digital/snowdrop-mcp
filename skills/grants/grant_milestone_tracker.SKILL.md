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
| `grant_id` | `string` | Yes | Unique identifier for the grant (e.g. "GNT-2026-001"). |
| `milestones` | `array` | Yes | List of milestone objects, each with `title` (string), `due_date` (ISO8601 date string), `status` (string: "pending", "complete", "overdue"), and `disbursement_usd` (float). |

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
    "grant_id": "GNT-2026-001",
    "milestones": [
      {"title": "Launch MVP", "due_date": "2026-03-01", "status": "complete", "disbursement_usd": 5000},
      {"title": "Q2 Report", "due_date": "2026-06-30", "status": "pending", "disbursement_usd": 3000}
    ]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "grant_milestone_tracker"`.
