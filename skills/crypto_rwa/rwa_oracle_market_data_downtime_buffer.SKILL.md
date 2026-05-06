---
skill: rwa_oracle_market_data_downtime_buffer
category: crypto_rwa
description: Projects NAV impact when core venues go dark and oracles rely on stale buffers.
tier: free
inputs: payload
---

# Rwa Oracle Market Data Downtime Buffer

## Description
Projects NAV impact when core venues go dark and oracles rely on stale buffers.

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
  "tool": "rwa_oracle_market_data_downtime_buffer",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_market_data_downtime_buffer"`.
