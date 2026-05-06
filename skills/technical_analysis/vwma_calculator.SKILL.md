---
skill: vwma_calculator
category: technical_analysis
description: Computes the volume-weighted moving average to compare price trends against standard SMA and confirm with volume.
tier: free
inputs: prices, volumes, period
---

# Vwma Calculator

## Description
Computes the volume-weighted moving average to compare price trends against standard SMA and confirm with volume.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Closing prices (oldest first). |
| `volumes` | `array` | Yes | Volume per period aligned with prices. |
| `period` | `integer` | Yes | Lookback window for VWMA. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "vwma_calculator",
  "arguments": {
    "prices": [],
    "volumes": [],
    "period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vwma_calculator"`.
