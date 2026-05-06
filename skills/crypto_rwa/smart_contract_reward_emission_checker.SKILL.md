---
skill: smart_contract_reward_emission_checker
category: crypto_rwa
description: Compares scheduled reward emissions to live supply to catch runaway inflation.
tier: free
inputs: none
---

# Smart Contract Reward Emission Checker

## Description
Compares scheduled reward emissions to live supply to catch runaway inflation.

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
  "tool": "smart_contract_reward_emission_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_reward_emission_checker"`.
