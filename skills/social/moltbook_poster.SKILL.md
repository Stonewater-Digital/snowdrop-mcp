---
skill: moltbook_poster
category: social
description: Formats Snowdrop skills for the Moltbook agent marketplace.
tier: free
inputs: skill_name, description, price_usd, category
---

# Moltbook Poster

## Description
Formats Snowdrop skills for the Moltbook agent marketplace.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skill_name` | `string` | Yes |  |
| `description` | `string` | Yes |  |
| `price_usd` | `number` | Yes |  |
| `category` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "moltbook_poster",
  "arguments": {
    "skill_name": "<skill_name>",
    "description": "<description>",
    "price_usd": 0,
    "category": "<category>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "moltbook_poster"`.
