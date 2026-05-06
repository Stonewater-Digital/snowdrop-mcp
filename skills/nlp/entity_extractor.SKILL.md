---
skill: entity_extractor
category: nlp
description: Uses regex heuristics to extract Snowdrop-relevant entities.
tier: free
inputs: text
---

# Entity Extractor

## Description
Uses regex heuristics to extract Snowdrop-relevant entities.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | `string` | Yes |  |
| `entity_types` | `array` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "entity_extractor",
  "arguments": {
    "text": "<text>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "entity_extractor"`.
