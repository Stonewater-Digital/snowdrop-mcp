---
skill: pricing_feed_voter
category: data_ingestion
description: Computes a consensus price across vendor feeds and flags quotes outside tolerance bands.
tier: free
inputs: quotes
---

# Pricing Feed Voter

## Description
Computes a consensus price across vendor feeds and flags quotes outside tolerance bands.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `quotes` | `array` | Yes | List of quotes containing source, price, and timestamp. |
| `method` | `string` | No | Voting method for consensus price calculation. |
| `spread_threshold_bps` | `number` | No | Absolute deviation threshold (in bps) before a quote is flagged. |
| `min_sources` | `integer` | No | Minimum number of valid quotes required to emit a price. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "pricing_feed_voter",
  "arguments": {
    "quotes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pricing_feed_voter"`.
