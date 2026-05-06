---
skill: firebase_realtime_db_write
category: root
description: Write or update a value in Firebase Realtime Database at the given path. Use method='set' to replace, 'update' to merge, 'push' to append.
tier: free
inputs: path, data
---

# Firebase Realtime Db Write

## Description
Write or update a value in Firebase Realtime Database at the given path. Use method='set' to replace, 'update' to merge, 'push' to append.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `string` | Yes |  |
| `data` | `object` | Yes |  |
| `method` | `string` | No |  |
| `database_url` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_realtime_db_write",
  "arguments": {
    "path": "<path>",
    "data": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_realtime_db_write"`.
