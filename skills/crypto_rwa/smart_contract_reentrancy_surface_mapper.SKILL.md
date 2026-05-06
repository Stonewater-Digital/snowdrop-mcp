---
skill: smart_contract_reentrancy_surface_mapper
category: crypto_rwa
description: Simulates nested calls and flags storage slots lacking reentrancy guards.
tier: free
inputs: payload
---

# Smart Contract Reentrancy Surface Mapper

## Description
Simulates nested calls and flags storage slots lacking reentrancy guards.

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
  "tool": "smart_contract_reentrancy_surface_mapper",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_reentrancy_surface_mapper"`.
