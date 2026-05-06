---
skill: rwa_treasury_sanctions_screen
category: crypto_rwa
description: Screens custodians and counterparties for OFAC flags before settlement.
tier: free
inputs: payload
---

# Rwa Treasury Sanctions Screen

## Description
Screens custodians and counterparties for OFAC flags before settlement.

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
  "tool": "rwa_treasury_sanctions_screen",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_treasury_sanctions_screen"`.
