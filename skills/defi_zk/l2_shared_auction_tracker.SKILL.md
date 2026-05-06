---
skill: l2_shared_auction_tracker
category: defi_zk
description: Aggregates shared sequencer auctions across major L2s to signal MEV demand.
tier: free
inputs: mempool_pressure_index, sandwich_alerts_last_hour, dex_slippage_bps
---

# L2 Shared Auction Tracker

## Description
Aggregates shared sequencer auctions across major L2s to signal MEV demand.

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
  "tool": "l2_shared_auction_tracker",
  "arguments": {
    "mempool_pressure_index": 0,
    "sandwich_alerts_last_hour": 0,
    "dex_slippage_bps": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "l2_shared_auction_tracker"`.
