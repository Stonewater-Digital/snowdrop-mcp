---
skill: firebase_remote_config_set
category: root
description: Publish a new Firebase Remote Config template. Merges provided parameters with existing config.
tier: free
inputs: none
---

# Firebase Remote Config Set

## Description
Publish a new Firebase Remote Config template. Merges provided parameters with existing config. Returns the new version number and update time.

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
  "tool": "firebase_remote_config_set",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_remote_config_set"`.
