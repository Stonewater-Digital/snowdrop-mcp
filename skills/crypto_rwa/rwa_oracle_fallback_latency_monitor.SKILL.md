---
skill: rwa_oracle_fallback_latency_monitor
category: crypto_rwa
description: Measures latency when feeds fall back to secondary providers during outages.
tier: free
inputs: payload
---

# Rwa Oracle Fallback Latency Monitor

## Description
Measures latency when feeds fall back to secondary providers during outages.

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
  "tool": "rwa_oracle_fallback_latency_monitor",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_fallback_latency_monitor"`.
