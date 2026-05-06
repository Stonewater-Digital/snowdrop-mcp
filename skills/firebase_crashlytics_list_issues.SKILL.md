---
skill: firebase_crashlytics_list_issues
category: root
description: List crash issues from Firebase Crashlytics for a given app. Returns issue ID, title, impact (users affected), and last occurrence time.
tier: free
inputs: app_id
---

# Firebase Crashlytics List Issues

## Description
List crash issues from Firebase Crashlytics for a given app. Returns issue ID, title, impact (users affected), and last occurrence time.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `app_id` | `string` | Yes |  |
| `project_id` | `string` | No |  |
| `page_size` | `integer` | No |  |
| `state` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_crashlytics_list_issues",
  "arguments": {
    "app_id": "<app_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_crashlytics_list_issues"`.
