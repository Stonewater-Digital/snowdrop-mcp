---
skill: parabolic_sar
category: technical_analysis
description: Implements Welles Wilder's Parabolic SAR with configurable acceleration factors to trail price trends.
tier: free
inputs: highs, lows, closes, af_start, af_step, af_max
---

# Parabolic Sar

## Description
Implements Welles Wilder's Parabolic SAR with configurable acceleration factors to trail price trends.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | Session highs, chronological. |
| `lows` | `array` | Yes | Session lows aligned with highs. |
| `closes` | `array` | Yes | Closing prices used to infer initial trend. |
| `af_start` | `number` | Yes | Initial acceleration factor (default 0.02). |
| `af_step` | `number` | Yes | Step increment when new extremes are set. |
| `af_max` | `number` | Yes | Maximum acceleration factor cap. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "parabolic_sar",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": [],
    "af_start": 0,
    "af_step": 0,
    "af_max": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "parabolic_sar"`.
