---
skill: rwa_oracle_energy_ppa_price_monitor
category: crypto_rwa
description: Monitors PPA settlement curves versus on-chain kilowatt-hour pricing oracles.
tier: free
inputs: payload
---

# Rwa Oracle Energy Ppa Price Monitor

## Description
Monitors PPA settlement curves versus on-chain kilowatt-hour pricing oracles.

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
  "tool": "rwa_oracle_energy_ppa_price_monitor",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_energy_ppa_price_monitor"`.
