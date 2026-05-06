---
skill: rwa_oracle_energy_ppa_price_monitor
category: crypto_rwa
description: Monitors PPA settlement curves versus on-chain kilowatt-hour pricing oracles.
tier: free
inputs: none
---

# Rwa Oracle Energy Ppa Price Monitor

## Description
Monitors PPA settlement curves versus on-chain kilowatt-hour pricing oracles.

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_oracle_energy_ppa_price_monitor",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_energy_ppa_price_monitor"`.
