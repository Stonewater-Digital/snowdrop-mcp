---
skill: rwa_oracle_cds_spread_checker
category: crypto_rwa
description: Checks corporate CDS spreads feeding private credit tokens for stale data.
tier: free
inputs: payload
---

# Rwa Oracle Cds Spread Checker

## Description
Checks corporate CDS spreads feeding private credit tokens for stale data.

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
  "tool": "rwa_oracle_cds_spread_checker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_cds_spread_checker"`.
