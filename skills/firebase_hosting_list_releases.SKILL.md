---
skill: firebase_hosting_list_releases
category: root
description: List release history for a Firebase Hosting site or channel. Returns list of releases with version, create_time, and status.
tier: free
inputs: none
---

# Firebase Hosting List Releases

## Description
List release history for a Firebase Hosting site or channel. Returns list of releases with version, create_time, and status.

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
  "tool": "firebase_hosting_list_releases",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_hosting_list_releases"`.
