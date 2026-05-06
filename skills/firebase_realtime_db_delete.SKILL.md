---
skill: firebase_realtime_db_delete
category: root
description: Delete a node from Firebase Realtime Database at the given path.
tier: free
inputs: none
---

# Firebase Realtime Db Delete

## Description
Delete a node from Firebase Realtime Database at the given path.

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
  "tool": "firebase_realtime_db_delete",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_realtime_db_delete"`.
