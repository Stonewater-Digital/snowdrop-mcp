---
skill: deprecation_notice_generator
category: api_versioning
description: Formats structured deprecation notices for skills/endpoints.
tier: free
inputs: deprecated_items
---

# Deprecation Notice Generator

## Description
Formats structured deprecation notices for skills/endpoints.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `deprecated_items` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "deprecation_notice_generator",
  "arguments": {
    "deprecated_items": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "deprecation_notice_generator"`.
