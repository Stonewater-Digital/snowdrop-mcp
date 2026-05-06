---
skill: carried_interest_tracker
category: fund_accounting
description: Tracks cumulative GP carried interest earned, distributed, and held in reserve based on fund cash flows. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Carried Interest Tracker

## Description
Tracks cumulative GP carried interest earned, distributed, and held in reserve based on fund cash flows. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "carried_interest_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "carried_interest_tracker"`.
