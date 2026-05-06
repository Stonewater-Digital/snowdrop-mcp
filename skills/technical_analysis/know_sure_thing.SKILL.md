---
skill: know_sure_thing
category: technical_analysis
description: Implements Martin Pring's KST oscillator via four smoothed rate-of-change components.
tier: free
inputs: prices, roc_periods, sma_periods, signal_period
---

# Know Sure Thing

## Description
Implements Martin Pring's KST oscillator via four smoothed rate-of-change components.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Price series. |
| `roc_periods` | `array` | Yes | List of ROC lookbacks (e.g., [10,15,20,30]). |
| `sma_periods` | `array` | Yes | List of SMA smoothings for each ROC. |
| `signal_period` | `integer` | Yes | Signal SMA for KST (default 9). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "know_sure_thing",
  "arguments": {
    "prices": [],
    "roc_periods": [],
    "sma_periods": [],
    "signal_period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "know_sure_thing"`.
