---
skill: rwa_oracle_t_bill_fx_cross_checker
category: crypto_rwa
description: Ensures T-bill tokens priced in non-USD denominations reflect live FX crosses.
tier: free
inputs: payload
---

# Rwa Oracle T Bill Fx Cross Checker

## Description
Ensures T-bill tokens priced in non-USD denominations reflect live FX crosses.

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
  "tool": "rwa_oracle_t_bill_fx_cross_checker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_t_bill_fx_cross_checker"`.
