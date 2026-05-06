---
skill: model_router
category: orchestration
description: Reads config/config.yaml and maps a task category to the correct model entry.
tier: free
inputs: none
---

# Model Router

## Description
Reads config/config.yaml and maps a task category to the correct model entry.

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
  "tool": "model_router",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "model_router"`.
