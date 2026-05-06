---
skill: firebase_app_distribution_upload
category: root
description: Upload a build artifact to Firebase App Distribution and notify testers. Returns the release name and download URL.
tier: free
inputs: app_id, binary_base64
---

# Firebase App Distribution Upload

## Description
Upload a build artifact to Firebase App Distribution and notify testers. Returns the release name and download URL.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `app_id` | `string` | Yes |  |
| `binary_base64` | `string` | Yes |  |
| `release_notes` | `string` | No |  |
| `tester_emails` | `any` | No |  |
| `group_aliases` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_app_distribution_upload",
  "arguments": {
    "app_id": "<app_id>",
    "binary_base64": "<binary_base64>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_app_distribution_upload"`.
