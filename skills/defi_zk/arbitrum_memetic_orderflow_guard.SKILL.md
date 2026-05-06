---
skill: arbitrum_memetic_orderflow_guard
category: defi_zk
description: Flags memecoin orderflow on Arbitrum attracting MEV dogpiles.
tier: free
inputs: mempool_pressure_index, sandwich_alerts_last_hour, dex_slippage_bps
---

# Arbitrum Memetic Orderflow Guard

## Description
Flags memecoin orderflow on Arbitrum attracting MEV dogpiles.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mempool_pressure_index` | `number` | Yes | 0-2 proxy for mempool load. |
| `sandwich_alerts_last_hour` | `number` | Yes | Count of sandwich alerts triggered in the last hour. |
| `dex_slippage_bps` | `number` | Yes | Observed slippage (bps) from tracked DEX pools. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "arbitrum_memetic_orderflow_guard",
  "arguments": {
    "mempool_pressure_index": 0,
    "sandwich_alerts_last_hour": 0,
    "dex_slippage_bps": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "arbitrum_memetic_orderflow_guard"`.
