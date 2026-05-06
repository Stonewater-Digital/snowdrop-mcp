---
skill: smart_contract_paymaster_abuse_detector
category: crypto_rwa
description: Analyzes ERC-4337 paymaster policies for unlimited sponsor risk.
tier: free
inputs: payload
---

# Smart Contract Paymaster Abuse Detector

## Description
Analyzes ERC-4337 paymaster policies for unlimited sponsor risk.

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
  "tool": "smart_contract_paymaster_abuse_detector",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_paymaster_abuse_detector"`.
