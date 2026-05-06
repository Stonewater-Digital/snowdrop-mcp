---
skill: rwa_oracle_inflation_swap_bridge
category: crypto_rwa
description: Maps inflation swap fixings to CPI-linked RWA oracle inputs.
tier: free
inputs: payload
---

# Rwa Oracle Inflation Swap Bridge

## Description
Maps inflation swap fixings to CPI-linked RWA oracle inputs.

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
  "tool": "rwa_oracle_inflation_swap_bridge",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_inflation_swap_bridge"`.
