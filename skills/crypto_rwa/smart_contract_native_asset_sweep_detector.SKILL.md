---
skill: smart_contract_native_asset_sweep_detector
category: crypto_rwa
description: Ensures no function can sweep native chain assets without quorum approval.
tier: free
inputs: payload
---

# Smart Contract Native Asset Sweep Detector

## Description
Ensures no function can sweep native chain assets without quorum approval.

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
  "tool": "smart_contract_native_asset_sweep_detector",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_native_asset_sweep_detector"`.
