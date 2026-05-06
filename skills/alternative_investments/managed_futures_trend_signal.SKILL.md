---
skill: managed_futures_trend_signal
category: alternative_investments
description: Computes normalized trend-following signals using short/medium/long moving averages and breakout statistics inspired by CTA models. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Managed Futures Trend Signal

## Description
Computes normalized trend-following signals using short/medium/long moving averages and breakout statistics inspired by CTA models. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "managed_futures_trend_signal",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "managed_futures_trend_signal"`.
