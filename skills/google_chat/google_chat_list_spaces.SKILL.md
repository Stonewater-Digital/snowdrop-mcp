---
skill: google_chat_list_spaces
category: google_chat
description: List Google Chat spaces accessible to the authenticated user.
tier: free
inputs: none
---

# Google Chat List Spaces

## Description
List Google Chat spaces accessible to the authenticated user.

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
  "tool": "google_chat_list_spaces",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "google_chat_list_spaces"`.
