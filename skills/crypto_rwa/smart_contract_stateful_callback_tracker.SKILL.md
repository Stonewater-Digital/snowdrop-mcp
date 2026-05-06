---
skill: smart_contract_stateful_callback_tracker
category: crypto_rwa
description: Tracks callbacks to ensure downstream states revert when upstream calls fail.
tier: free
inputs: payload
---

# Smart Contract Stateful Callback Tracker

## Description
Tracks callbacks to ensure downstream states revert when upstream calls fail.

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
  "tool": "smart_contract_stateful_callback_tracker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_stateful_callback_tracker"`.
