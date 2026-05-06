---
skill: smart_contract_unbounded_loop_detector
category: crypto_rwa
description: Scans bytecode for unbounded loops that can be griefed via block gas limits.
tier: free
inputs: payload
---

# Smart Contract Unbounded Loop Detector

## Description
Scans bytecode for unbounded loops that can be griefed via block gas limits.

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
  "tool": "smart_contract_unbounded_loop_detector",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_unbounded_loop_detector"`.
