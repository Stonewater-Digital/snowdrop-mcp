---
skill: firebase_storage_upload
category: root
description: Upload a base64-encoded file to Firebase Cloud Storage. Returns the storage path and a signed download URL valid for 7 days.
tier: free
inputs: destination_path, content_base64
---

# Firebase Storage Upload

## Description
Upload a base64-encoded file to Firebase Cloud Storage. Returns the storage path and a signed download URL valid for 7 days.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `destination_path` | `string` | Yes |  |
| `content_base64` | `string` | Yes |  |
| `content_type` | `string` | No |  |
| `bucket_name` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_storage_upload",
  "arguments": {
    "destination_path": "<destination_path>",
    "content_base64": "<content_base64>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_storage_upload"`.
