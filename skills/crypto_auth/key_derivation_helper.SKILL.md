---
skill: key_derivation_helper
category: crypto_auth
description: Derives deterministic key identifiers from the master seed.
tier: free
inputs: purpose, context
---

# Key Derivation Helper

## Description
Derives deterministic key identifiers from the master seed.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `purpose` | `string` | Yes |  |
| `context` | `string` | Yes | Context string such as agent_id or service name. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "key_derivation_helper",
  "arguments": {
    "purpose": "<purpose>",
    "context": "<context>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "key_derivation_helper"`.
