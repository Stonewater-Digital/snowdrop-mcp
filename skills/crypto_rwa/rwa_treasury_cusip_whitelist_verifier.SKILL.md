---
skill: rwa_treasury_cusip_whitelist_verifier
category: crypto_rwa
description: Ensures only approved CUSIPs appear in wrapped Treasury vaults by reconciling mint payloads with issuance calendars.
tier: free
inputs: payload
---

# Rwa Treasury Cusip Whitelist Verifier

## Description
Ensures only approved CUSIPs appear in wrapped Treasury vaults by reconciling mint payloads with issuance calendars.

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
  "tool": "rwa_treasury_cusip_whitelist_verifier",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_treasury_cusip_whitelist_verifier"`.
