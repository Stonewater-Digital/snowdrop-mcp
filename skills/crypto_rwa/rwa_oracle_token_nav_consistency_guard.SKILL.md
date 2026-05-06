---
skill: rwa_oracle_token_nav_consistency_guard
category: crypto_rwa
description: Confirms oracle NAV outputs reconcile with issuer-reported NAV statements.
tier: free
inputs: none
---

# Rwa Oracle Token Nav Consistency Guard

## Description
Confirms oracle NAV outputs reconcile with issuer-reported NAV statements.

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
  "tool": "rwa_oracle_token_nav_consistency_guard",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_token_nav_consistency_guard"`.
