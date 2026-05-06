---
skill: blog_post_generator
category: content
description: Creates structured blog content with title, sections, and metadata.
tier: free
inputs: topic, audience, key_points
---

# Blog Post Generator

## Description
Creates structured blog content with title, sections, and metadata.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `topic` | `string` | Yes |  |
| `audience` | `string` | Yes |  |
| `key_points` | `array` | Yes |  |
| `tone` | `string` | No |  |
| `word_count` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "blog_post_generator",
  "arguments": {
    "topic": "<topic>",
    "audience": "<audience>",
    "key_points": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "blog_post_generator"`.
