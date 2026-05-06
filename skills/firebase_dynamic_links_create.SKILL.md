---
skill: firebase_dynamic_links_create
category: root
description: Create a Firebase Dynamic Link (short URL) that routes users to the correct app or web destination based on their platform. Returns the short link and preview link.
tier: free
inputs: none
---

# Firebase Dynamic Links Create

## Description
Create a Firebase Dynamic Link (short URL) that routes users to the correct app or web destination based on their platform. Returns the short link and preview link.

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
  "tool": "firebase_dynamic_links_create",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_dynamic_links_create"`.
