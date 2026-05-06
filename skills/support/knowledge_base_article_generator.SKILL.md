---
skill: knowledge_base_article_generator
category: support
description: Summarizes frequent ticket resolutions into KB articles to reduce load.
tier: free
inputs: resolved_tickets
---

# Knowledge Base Article Generator

## Description
Summarizes frequent ticket resolutions into KB articles to reduce load.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `resolved_tickets` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "knowledge_base_article_generator",
  "arguments": {
    "resolved_tickets": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "knowledge_base_article_generator"`.
