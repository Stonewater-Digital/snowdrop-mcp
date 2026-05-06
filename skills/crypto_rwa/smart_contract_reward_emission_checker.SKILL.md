---
skill: smart_contract_reward_emission_checker
category: crypto_rwa
description: Compares scheduled reward emissions to live supply to catch runaway inflation.
tier: free
inputs: payload
---

# Smart Contract Reward Emission Checker

## Description
Compares scheduled reward emissions to live supply to catch runaway inflation.

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
  "tool": "smart_contract_reward_emission_checker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_reward_emission_checker"`.
