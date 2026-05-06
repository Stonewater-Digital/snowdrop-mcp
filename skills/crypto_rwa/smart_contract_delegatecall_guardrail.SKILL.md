---
skill: smart_contract_delegatecall_guardrail
category: crypto_rwa
description: Inspects delegatecall targets to ensure they respect access control and immutability assumptions.
tier: free
inputs: payload
---

# Smart Contract Delegatecall Guardrail

## Description
Inspects delegatecall targets to ensure they respect access control and immutability assumptions.

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
  "tool": "smart_contract_delegatecall_guardrail",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_delegatecall_guardrail"`.
