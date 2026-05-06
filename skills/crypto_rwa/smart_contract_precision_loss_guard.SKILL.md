---
skill: smart_contract_precision_loss_guard
category: crypto_rwa
description: Checks decimal math routines to prevent precision loss on rebasing assets.
tier: free
inputs: none
---

# Smart Contract Precision Loss Guard

## Description
Checks decimal math routines to prevent precision loss on rebasing assets.

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
  "tool": "smart_contract_precision_loss_guard",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_precision_loss_guard"`.
