---
skill: ichimoku_cloud
category: technical_analysis
description: Generates Ichimoku Kinko Hyo components (Tenkan, Kijun, Senkou A/B, Chikou) for full cloud analysis.
tier: free
inputs: highs, lows, closes, tenkan, kijun, senkou_b, chikou
---

# Ichimoku Cloud

## Description
Generates Ichimoku Kinko Hyo components (Tenkan, Kijun, Senkou A/B, Chikou) for full cloud analysis.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High prices. |
| `lows` | `array` | Yes | Low prices. |
| `closes` | `array` | Yes | Closing prices. |
| `tenkan` | `integer` | Yes | Tenkan-sen lookback (default 9). |
| `kijun` | `integer` | Yes | Kijun-sen lookback (default 26). |
| `senkou_b` | `integer` | Yes | Senkou Span B lookback (default 52). |
| `chikou` | `integer` | Yes | Chikou span offset (default 26). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ichimoku_cloud",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": [],
    "tenkan": 0,
    "kijun": 0,
    "senkou_b": 0,
    "chikou": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ichimoku_cloud"`.
