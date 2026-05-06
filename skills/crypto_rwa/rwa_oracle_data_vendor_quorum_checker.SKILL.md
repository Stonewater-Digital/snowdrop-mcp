---
skill: rwa_oracle_data_vendor_quorum_checker
category: crypto_rwa
description: Ensures quorum logic across multiple vendors is functioning and weighted correctly.
tier: free
inputs: payload
---

# Rwa Oracle Data Vendor Quorum Checker

## Description
Ensures quorum logic across multiple vendors is functioning and weighted correctly.

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
  "tool": "rwa_oracle_data_vendor_quorum_checker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_data_vendor_quorum_checker"`.
