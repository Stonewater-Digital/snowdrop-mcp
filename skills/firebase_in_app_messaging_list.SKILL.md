---
skill: firebase_in_app_messaging_list
category: root
description: List active Firebase In-App Messaging campaigns for a project. Returns campaign names, trigger conditions, and message content.
tier: free
inputs: none
---

# Firebase In App Messaging List

## Description
List active Firebase In-App Messaging campaigns for a project. Returns campaign names, trigger conditions, and message content.

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
  "tool": "firebase_in_app_messaging_list",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_in_app_messaging_list"`.
