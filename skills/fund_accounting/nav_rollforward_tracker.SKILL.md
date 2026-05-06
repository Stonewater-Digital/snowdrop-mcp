---
skill: nav_rollforward_tracker
category: fund_accounting
description: Bridges opening NAV to closing NAV using period cash flows and valuation changes. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Nav Rollforward Tracker

## Description
Bridges opening NAV to closing NAV using period cash flows and valuation changes. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "nav_rollforward_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "nav_rollforward_tracker"`.
