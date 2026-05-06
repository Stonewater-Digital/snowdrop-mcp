---
skill: smart_contract_signature_malleability_scan
category: crypto_rwa
description: Checks signature verification logic for malleability or unchecked parameters.
tier: free
inputs: payload
---

# Smart Contract Signature Malleability Scan

## Description
Checks signature verification logic for malleability or unchecked parameters.

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
  "tool": "smart_contract_signature_malleability_scan",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_signature_malleability_scan"`.
