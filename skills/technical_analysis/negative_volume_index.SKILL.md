---
skill: negative_volume_index
category: technical_analysis
description: Computes the Negative Volume Index with a 255-day EMA signal line per Norman Fosback.
tier: free
inputs: closes, volumes
---

# Negative Volume Index

## Description
Computes the Negative Volume Index with a 255-day EMA signal line per Norman Fosback.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `closes` | `array` | Yes | Close prices. |
| `volumes` | `array` | Yes | Volume per session. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "negative_volume_index",
  "arguments": {
    "closes": [],
    "volumes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "negative_volume_index"`.
