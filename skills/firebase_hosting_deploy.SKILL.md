---
skill: firebase_hosting_deploy
category: root
description: Deploy files to a Firebase Hosting site or channel via the Firebase Hosting REST API. Returns the channel URL and release version.
tier: free
inputs: none
---

# Firebase Hosting Deploy

## Description
Deploy files to a Firebase Hosting site or channel via the Firebase Hosting REST API. Returns the channel URL and release version.

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
  "tool": "firebase_hosting_deploy",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_hosting_deploy"`.
