---
skill: key_rate_duration
category: fixed_income_analytics
description: Computes key rate durations by bumping individual zero buckets (1/2/5/10/20/30y) consistent with the Basel IRRBB supervisory outlier test. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Key Rate Duration

## Description
Computes key rate durations by bumping individual zero buckets (1/2/5/10/20/30y) consistent with the Basel IRRBB supervisory outlier test. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "key_rate_duration",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "key_rate_duration"`.
