---
skill: rwa_private_credit_covenant_packet_checker
category: crypto_rwa
description: Parses covenant reports to ensure breach notices trigger token gating logic.
tier: free
inputs: payload
---

# Rwa Private Credit Covenant Packet Checker

## Description
Parses covenant reports to ensure breach notices trigger token gating logic.

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
  "tool": "rwa_private_credit_covenant_packet_checker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_private_credit_covenant_packet_checker"`.
