---
skill: rwa_oracle_volume_weight_consistency
category: crypto_rwa
description: Ensures oracle VWAP calculations match reported venue volumes.
tier: free
inputs: none
---

# Rwa Oracle Volume Weight Consistency

## Description
Ensures oracle VWAP calculations match reported venue volumes.

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
  "tool": "rwa_oracle_volume_weight_consistency",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_volume_weight_consistency"`.
