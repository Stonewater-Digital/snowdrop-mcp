---
skill: skill_review_pipeline
category: skill_marketplace
description: Runs static review checks on submitted community skill code.
tier: free
inputs: submission_id, skill_code
---

# Skill Review Pipeline

## Description
Runs static review checks on submitted community skill code.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `submission_id` | `string` | Yes |  |
| `skill_code` | `string` | Yes |  |
| `checklist` | `['object', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "skill_review_pipeline",
  "arguments": {
    "submission_id": "<submission_id>",
    "skill_code": "<skill_code>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skill_review_pipeline"`.
