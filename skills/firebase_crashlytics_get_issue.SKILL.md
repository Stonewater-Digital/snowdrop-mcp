---
skill: firebase_crashlytics_get_issue
category: root
description: Get detailed information about a specific Firebase Crashlytics issue including stack trace summary and affected versions.
tier: free
inputs: none
---

# Firebase Crashlytics Get Issue

## Description
Get detailed information about a specific Firebase Crashlytics issue including stack trace summary and affected versions.

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
  "tool": "firebase_crashlytics_get_issue",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_crashlytics_get_issue"`.
