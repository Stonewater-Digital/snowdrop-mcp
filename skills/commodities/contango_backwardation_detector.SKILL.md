---
skill: contango_backwardation_detector
category: commodities
description: Identifies curve structure (contango / backwardation / mixed), computes per-tenor annualized roll yield, front and tail basis, and flags extreme backwardation.
tier: free
inputs: spot_price, futures_prices
---

# Contango Backwardation Detector

## Description
Identifies curve structure (contango / backwardation / mixed), computes per-tenor annualized roll yield, front and tail basis, and flags extreme backwardation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spot_price` | `number` | Yes | Current spot price (must be > 0). |
| `futures_prices` | `array` | Yes | Futures contracts ordered by tenor. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "contango_backwardation_detector",
  "arguments": {
    "spot_price": 0,
    "futures_prices": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "contango_backwardation_detector"`.
