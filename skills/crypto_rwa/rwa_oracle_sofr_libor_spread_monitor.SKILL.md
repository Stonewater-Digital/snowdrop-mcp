---
skill: rwa_oracle_sofr_libor_spread_monitor
category: crypto_rwa
description: Tracks SOFR-LIBOR spreads embedded in oracle discount factors for loans.
tier: free
inputs: payload
---

# Rwa Oracle Sofr Libor Spread Monitor

## Description
Tracks SOFR-LIBOR spreads embedded in oracle discount factors for loans.

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
  "tool": "rwa_oracle_sofr_libor_spread_monitor",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_sofr_libor_spread_monitor"`.
