---
skill: firebase_realtime_db_read
category: root
description: Read a value from Firebase Realtime Database at the given path. Returns the value as JSON.
tier: free
inputs: path
---

# Firebase Realtime Db Read

## Description
Read a value from Firebase Realtime Database at the given path. Returns the value as JSON.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `string` | Yes |  |
| `database_url` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_realtime_db_read",
  "arguments": {
    "path": "<path>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_realtime_db_read"`.
