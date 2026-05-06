---
skill: firebase_storage_upload
category: root
description: Upload a base64-encoded file to Firebase Cloud Storage. Returns the storage path and a signed download URL valid for 7 days.
tier: free
inputs: none
---

# Firebase Storage Upload

## Description
Upload a base64-encoded file to Firebase Cloud Storage. Returns the storage path and a signed download URL valid for 7 days.

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_storage_upload",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_storage_upload"`.
