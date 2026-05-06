---
skill: contract_lifecycle_manager
category: contracts_lifecycle
description: Creates, updates, lists, and surfaces contracts nearing expiration.
tier: free
inputs: operation
---

# Contract Lifecycle Manager

## Description
Creates, updates, lists, and surfaces contracts nearing expiration.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `contract` | `object` | No |  |
| `lookahead_days` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "contract_lifecycle_manager",
  "arguments": {
    "operation": "<operation>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "contract_lifecycle_manager"`.
