---
skill: rwa_oracle_block_timestamp_gapper
category: crypto_rwa
description: Measures block timestamp gaps affecting TWAP-driven oracle updates.
tier: free
inputs: payload
---

# Rwa Oracle Block Timestamp Gapper

## Description
Measures block timestamp gaps affecting TWAP-driven oracle updates.

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
  "tool": "rwa_oracle_block_timestamp_gapper",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_block_timestamp_gapper"`.
