---
skill: smart_contract_native_asset_sweep_detector
category: crypto_rwa
description: Ensures no function can sweep native chain assets without quorum approval.
tier: free
inputs: none
---

# Smart Contract Native Asset Sweep Detector

## Description
Ensures no function can sweep native chain assets without quorum approval.

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
  "tool": "smart_contract_native_asset_sweep_detector",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_native_asset_sweep_detector"`.
