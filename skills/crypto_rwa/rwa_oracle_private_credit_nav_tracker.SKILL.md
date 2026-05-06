---
skill: rwa_oracle_private_credit_nav_tracker
category: crypto_rwa
description: Aggregates private credit NAV statements and reconciles them with streaming oracle NAVs.
tier: free
inputs: payload
---

# Rwa Oracle Private Credit Nav Tracker

## Description
Aggregates private credit NAV statements and reconciles them with streaming oracle NAVs.

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
  "tool": "rwa_oracle_private_credit_nav_tracker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_private_credit_nav_tracker"`.
