---
skill: rwa_oracle_primary_secondary_spread_checker
category: crypto_rwa
description: Compares primary issuance prices with secondary token trading to spot gaps.
tier: free
inputs: payload
---

# Rwa Oracle Primary Secondary Spread Checker

## Description
Compares primary issuance prices with secondary token trading to spot gaps.

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
  "tool": "rwa_oracle_primary_secondary_spread_checker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_primary_secondary_spread_checker"`.
