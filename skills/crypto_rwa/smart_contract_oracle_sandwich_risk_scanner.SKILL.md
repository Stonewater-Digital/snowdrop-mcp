---
skill: smart_contract_oracle_sandwich_risk_scanner
category: crypto_rwa
description: Identifies oracle updates that traders can sandwich before settlement.
tier: free
inputs: payload
---

# Smart Contract Oracle Sandwich Risk Scanner

## Description
Identifies oracle updates that traders can sandwich before settlement.

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
  "tool": "smart_contract_oracle_sandwich_risk_scanner",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_oracle_sandwich_risk_scanner"`.
