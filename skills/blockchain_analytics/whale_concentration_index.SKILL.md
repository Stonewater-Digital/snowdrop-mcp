---
skill: whale_concentration_index
category: blockchain_analytics
description: Evaluates distribution of balances to understand whale dominance and decentralization risk.
tier: free
inputs: balances
---

# Whale Concentration Index

## Description
Evaluates distribution of balances to understand whale dominance and decentralization risk.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `balances` | `array` | Yes | List of wallet balances in descending order (raw tokens or USD). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "whale_concentration_index",
  "arguments": {
    "balances": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "whale_concentration_index"`.
