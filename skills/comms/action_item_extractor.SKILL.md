---
skill: action_item_extractor
category: comms
description: Uses heuristics to identify action items, assignees, and priority from text.
tier: free
inputs: text
---

# Action Item Extractor

## Description
Uses heuristics to identify action items, assignees, and priority from text.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | `string` | Yes |  |
| `participants` | `array` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "action_item_extractor",
  "arguments": {
    "text": "<text>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "action_item_extractor"`.
