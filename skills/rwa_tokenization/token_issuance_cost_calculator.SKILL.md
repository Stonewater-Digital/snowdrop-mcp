---
skill: token_issuance_cost_calculator
category: rwa_tokenization
description: Aggregates issuance cost buckets and derives per-token cost of capital.
tier: free
inputs: legal_cost, audit_cost, marketing_cost, platform_fee, tokens_issued
---

# Token Issuance Cost Calculator

## Description
Aggregates issuance cost buckets and derives per-token cost of capital.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `legal_cost` | `number` | Yes | Legal and structuring fees |
| `audit_cost` | `number` | Yes | Audit and attestation fees |
| `marketing_cost` | `number` | Yes | Distribution and marketing spend |
| `platform_fee` | `number` | Yes | Platform fee charged by issuance partner |
| `tokens_issued` | `number` | Yes | Number of tokens minted |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_issuance_cost_calculator",
  "arguments": {
    "legal_cost": 0,
    "audit_cost": 0,
    "marketing_cost": 0,
    "platform_fee": 0,
    "tokens_issued": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_issuance_cost_calculator"`.
