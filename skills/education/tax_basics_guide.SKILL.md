---
skill: tax_basics_guide
category: education
description: Shares plain-language US tax basics by entity type (goodwill only).
tier: free
inputs: entity_type, topic
---

# Tax Basics Guide

## Description
Shares plain-language US tax basics by entity type (goodwill only).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `entity_type` | `string` | Yes |  |
| `topic` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tax_basics_guide",
  "arguments": {
    "entity_type": "<entity_type>",
    "topic": "<topic>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tax_basics_guide"`.
