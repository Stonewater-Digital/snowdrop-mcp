---
skill: long_term_memory_store
category: memory
description: Append-only JSONL memory store with taggable search and CRUD operations.
tier: free
inputs: operation, key
---

# Long Term Memory Store

## Description
Append-only JSONL memory store with taggable search and CRUD operations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `key` | `string` | Yes |  |
| `value` | `['object', 'array', 'string', 'number', 'boolean', 'null']` | No |  |
| `tags` | `array` | No | Semantic tags for retrieval |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "long_term_memory_store",
  "arguments": {
    "operation": "<operation>",
    "key": "<key>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "long_term_memory_store"`.
