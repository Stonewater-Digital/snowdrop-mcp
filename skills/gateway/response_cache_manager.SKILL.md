---
skill: response_cache_manager
category: gateway
description: Provides get/set/invalidate operations for skill response cache entries.
tier: free
inputs: operation, cache_key
---

# Response Cache Manager

## Description
Provides get/set/invalidate operations for skill response cache entries.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `cache_key` | `string` | Yes |  |
| `value` | `['object', 'null']` | No |  |
| `ttl_seconds` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "response_cache_manager",
  "arguments": {
    "operation": "<operation>",
    "cache_key": "<cache_key>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "response_cache_manager"`.
