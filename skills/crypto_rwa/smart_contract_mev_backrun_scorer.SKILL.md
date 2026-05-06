---
skill: smart_contract_mev_backrun_scorer
category: crypto_rwa
description: Scores how easily transactions can be backrun given hooks and mempool patterns.
tier: free
inputs: none
---

# Smart Contract Mev Backrun Scorer

## Description
Scores how easily transactions can be backrun given hooks and mempool patterns.

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
  "tool": "smart_contract_mev_backrun_scorer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_mev_backrun_scorer"`.
