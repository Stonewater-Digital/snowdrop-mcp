---
skill: rwa_oracle_private_credit_nav_tracker
category: crypto_rwa
description: Aggregates private credit NAV statements and reconciles them with streaming oracle NAVs.
tier: free
inputs: none
---

# Rwa Oracle Private Credit Nav Tracker

## Description
Aggregates private credit NAV statements and reconciles them with streaming oracle NAVs.

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_oracle_private_credit_nav_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_private_credit_nav_tracker"`.
