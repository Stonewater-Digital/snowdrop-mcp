---
skill: token_standard_beneficial_owner_registry_bridge
category: crypto_rwa
description: Bridges beneficial owner registries into token KYC proofs for regulators.
tier: free
inputs: payload
---

# Token Standard Beneficial Owner Registry Bridge

## Description
Bridges beneficial owner registries into token KYC proofs for regulators.

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
  "tool": "token_standard_beneficial_owner_registry_bridge",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_beneficial_owner_registry_bridge"`.
