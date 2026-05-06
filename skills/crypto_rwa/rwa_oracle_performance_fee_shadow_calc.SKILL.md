---
skill: rwa_oracle_performance_fee_shadow_calc
category: crypto_rwa
description: Runs independent performance-fee calculations to cross-check oracle output.
tier: free
inputs: payload
---

# Rwa Oracle Performance Fee Shadow Calc

## Description
Runs independent performance-fee calculations to cross-check oracle output.

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
  "tool": "rwa_oracle_performance_fee_shadow_calc",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_performance_fee_shadow_calc"`.
