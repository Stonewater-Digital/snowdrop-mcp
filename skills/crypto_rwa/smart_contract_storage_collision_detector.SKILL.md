---
skill: smart_contract_storage_collision_detector
category: crypto_rwa
description: Analyzes proxy storage layouts for slot collisions across upgrades.
tier: free
inputs: payload
---

# Smart Contract Storage Collision Detector

## Description
Analyzes proxy storage layouts for slot collisions across upgrades.

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
  "tool": "smart_contract_storage_collision_detector",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_storage_collision_detector"`.
