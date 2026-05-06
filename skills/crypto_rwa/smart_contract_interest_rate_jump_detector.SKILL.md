---
skill: smart_contract_interest_rate_jump_detector
category: crypto_rwa
description: Stress-tests rate models for discontinuities following governance votes.
tier: free
inputs: payload
---

# Smart Contract Interest Rate Jump Detector

## Description
Stress-tests rate models for discontinuities following governance votes.

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
  "tool": "smart_contract_interest_rate_jump_detector",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_interest_rate_jump_detector"`.
