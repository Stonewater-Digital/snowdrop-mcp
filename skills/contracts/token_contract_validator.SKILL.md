---
skill: token_contract_validator
category: contracts
description: Flags risky token authority settings and liquidity constraints.
tier: free
inputs: token
---

# Token Contract Validator

## Description
Flags risky token authority settings and liquidity constraints.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `token` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_contract_validator",
  "arguments": {
    "token": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_contract_validator"`.
