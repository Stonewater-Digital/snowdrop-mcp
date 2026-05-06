---
skill: smart_contract_mev_backrun_scorer
category: crypto_rwa
description: Scores how easily transactions can be backrun given hooks and mempool patterns.
tier: free
inputs: payload
---

# Smart Contract Mev Backrun Scorer

## Description
Scores how easily transactions can be backrun given hooks and mempool patterns.

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
  "tool": "smart_contract_mev_backrun_scorer",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_mev_backrun_scorer"`.
