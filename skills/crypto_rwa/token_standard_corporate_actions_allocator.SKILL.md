---
skill: token_standard_corporate_actions_allocator
category: crypto_rwa
description: Automates corporate action allocation tables for partitioned cap tables.
tier: free
inputs: payload
---

# Token Standard Corporate Actions Allocator

## Description
Automates corporate action allocation tables for partitioned cap tables.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_standard_corporate_actions_allocator",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_corporate_actions_allocator"`.
