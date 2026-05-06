---
skill: smart_contract_token_allowance_drift_checker
category: crypto_rwa
description: Monitors allowances versus expected spend to highlight risky approvals.
tier: free
inputs: none
---

# Smart Contract Token Allowance Drift Checker

## Description
Monitors allowances versus expected spend to highlight risky approvals.

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
  "tool": "smart_contract_token_allowance_drift_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_token_allowance_drift_checker"`.
