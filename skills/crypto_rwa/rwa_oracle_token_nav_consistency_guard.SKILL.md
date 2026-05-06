---
skill: rwa_oracle_token_nav_consistency_guard
category: crypto_rwa
description: Confirms oracle NAV outputs reconcile with issuer-reported NAV statements.
tier: free
inputs: payload
---

# Rwa Oracle Token Nav Consistency Guard

## Description
Confirms oracle NAV outputs reconcile with issuer-reported NAV statements.

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
  "tool": "rwa_oracle_token_nav_consistency_guard",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_token_nav_consistency_guard"`.
