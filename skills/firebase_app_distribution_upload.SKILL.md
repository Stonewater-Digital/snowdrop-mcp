---
skill: firebase_app_distribution_upload
category: root
description: Upload a build artifact to Firebase App Distribution and notify testers. Returns the release name and download URL.
tier: free
inputs: none
---

# Firebase App Distribution Upload

## Description
Upload a build artifact to Firebase App Distribution and notify testers. Returns the release name and download URL.

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
  "tool": "firebase_app_distribution_upload",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_app_distribution_upload"`.
