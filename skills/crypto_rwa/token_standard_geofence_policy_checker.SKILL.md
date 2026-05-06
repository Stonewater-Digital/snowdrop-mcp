---
skill: token_standard_geofence_policy_checker
category: crypto_rwa
description: Enforces geo-fencing policies at the smart-contract level before transfers settle.
tier: free
inputs: none
---

# Token Standard Geofence Policy Checker

## Description
Enforces geo-fencing policies at the smart-contract level before transfers settle.

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
  "tool": "token_standard_geofence_policy_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_geofence_policy_checker"`.
