---
skill: candidate_pipeline_tracker
category: recruiting
description: Manage candidate pipeline state in Firestore. Advance stages, reject, add notes, or list candidates.
tier: free
inputs: action
---

# Candidate Pipeline Tracker

## Description
Manage candidate pipeline state in Firestore. Advance stages, reject, add notes, or list candidates. All operations are idempotent with audit trail.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes |  |
| `trace_id` | `string` | No |  |
| `stage` | `string` | No |  |
| `reason` | `string` | No |  |
| `note` | `string` | No |  |
| `actor` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "candidate_pipeline_tracker",
  "arguments": {
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "candidate_pipeline_tracker"`.
