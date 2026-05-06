---
skill: firebase_crashlytics_get_issue
category: root
description: Get detailed information about a specific Firebase Crashlytics issue including stack trace summary and affected versions.
tier: free
inputs: app_id, issue_id
---

# Firebase Crashlytics Get Issue

## Description
Get detailed information about a specific Firebase Crashlytics issue including stack trace summary and affected versions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `app_id` | `string` | Yes |  |
| `issue_id` | `string` | Yes |  |
| `project_id` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_crashlytics_get_issue",
  "arguments": {
    "app_id": "<app_id>",
    "issue_id": "<issue_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_crashlytics_get_issue"`.
