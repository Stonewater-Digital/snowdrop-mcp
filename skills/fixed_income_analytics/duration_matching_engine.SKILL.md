---
skill: duration_matching_engine
category: fixed_income_analytics
description: Solves for asset weights whose duration and convexity match a target liability, using least-squares immunization per Fabozzi. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Duration Matching Engine

## Description
Solves for asset weights whose duration and convexity match a target liability, using least-squares immunization per Fabozzi. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "duration_matching_engine",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "duration_matching_engine"`.
