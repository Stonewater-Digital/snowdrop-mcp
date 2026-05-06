---
skill: knowledge_base_indexer
category: search
description: Builds an inverted index over documents and answers keyword queries.
tier: free
inputs: documents
---

# Knowledge Base Indexer

## Description
Builds an inverted index over documents and answers keyword queries.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `documents` | `array` | Yes |  |
| `query` | `['string', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "knowledge_base_indexer",
  "arguments": {
    "documents": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "knowledge_base_indexer"`.
