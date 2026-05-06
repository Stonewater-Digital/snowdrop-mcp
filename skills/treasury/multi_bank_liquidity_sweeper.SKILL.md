---
skill: multi_bank_liquidity_sweeper
category: treasury
description: Recommend cash sweeps across multiple banks using target min/max policies.
tier: free
inputs: accounts
---

# Multi Bank Liquidity Sweeper

## Description
Recommend cash sweeps across multiple banks using target min/max policies.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `accounts` | `array` | Yes | List with keys: bank, account_id, balance, target_min, target_max, sweep_destination. |
| `notify_thunder` | `boolean` | No | Escalate when aggregate deficit exceeds the policy threshold. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "multi_bank_liquidity_sweeper",
  "arguments": {
    "accounts": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "multi_bank_liquidity_sweeper"`.
