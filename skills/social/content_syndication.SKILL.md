---
skill: content_syndication
category: social
description: Take a core message or piece of content and produce platform-optimized versions for multiple channels at once: GitHub Discussion, Moltbook post, Twitter/X thread, Discord message. Each version is adapted for platform format, character limits, and audience expectations while keeping Snowdrop's voice consistent.
tier: free
inputs: core_message
---

# Content Syndication

## Description
Take a core message or piece of content and produce platform-optimized versions for multiple channels at once: GitHub Discussion, Moltbook post, Twitter/X thread, Discord message. Each version is adapted for platform format, character limits, and audience expectations while keeping Snowdrop's voice consistent. Dramatically speeds up cross-platform posting campaigns.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `core_message` | `string` | Yes |  |
| `platforms` | `array` | No |  |
| `goal` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "content_syndication",
  "arguments": {
    "core_message": "<core_message>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "content_syndication"`.
