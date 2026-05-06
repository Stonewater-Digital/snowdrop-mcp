---
skill: private_key_shard_manager
category: technical
description: MPC key shard management using Shamir's Secret Sharing: split a key into N shards (K-of-N required to reconstruct), reconstruct from K shards, or verify shard validity. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Private Key Shard Manager

## Description
MPC key shard management using Shamir's Secret Sharing: split a key into N shards (K-of-N required to reconstruct), reconstruct from K shards, or verify shard validity. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "private_key_shard_manager",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "private_key_shard_manager"`.
