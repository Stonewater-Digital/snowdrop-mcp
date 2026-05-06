---
skill: token_standard_audit_trail_packer
category: crypto_rwa
description: Packages on-chain and off-chain audit trails for regulator-ready exports.
tier: free
inputs: payload
---

# Token Standard Audit Trail Packer

## Description
Packages on-chain and off-chain audit trails for regulator-ready exports.

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
  "tool": "token_standard_audit_trail_packer",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_audit_trail_packer"`.
