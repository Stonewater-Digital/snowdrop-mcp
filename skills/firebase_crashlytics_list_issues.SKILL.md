---
skill: firebase_crashlytics_list_issues
category: root
description: List crash issues from Firebase Crashlytics for a given app. Returns issue ID, title, impact (users affected), and last occurrence time.
tier: free
inputs: none
---

# Firebase Crashlytics List Issues

## Description
List crash issues from Firebase Crashlytics for a given app. Returns issue ID, title, impact (users affected), and last occurrence time.

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
  "tool": "firebase_crashlytics_list_issues",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_crashlytics_list_issues"`.
