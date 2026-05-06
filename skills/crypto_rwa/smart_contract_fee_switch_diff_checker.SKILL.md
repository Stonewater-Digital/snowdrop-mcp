---
skill: smart_contract_fee_switch_diff_checker
category: crypto_rwa
description: Compares fee switch states across deployments to expose unnoticed toggles.
tier: free
inputs: none
---

# Smart Contract Fee Switch Diff Checker

## Description
Compares fee switch states across deployments to expose unnoticed toggles.

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
  "tool": "smart_contract_fee_switch_diff_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_fee_switch_diff_checker"`.
