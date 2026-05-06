---
skill: changelog_generator
category: docs
description: Outputs Keep a Changelog formatted text from change entries.
tier: free
inputs: changes
---

# Changelog Generator

## Description
Outputs Keep a Changelog formatted text from change entries.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `changes` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "changelog_generator",
  "arguments": {
    "changes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "changelog_generator"`.
