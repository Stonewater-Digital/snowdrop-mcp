---
skill: drawdown_scheduler
category: fund_accounting
description: Schedules capital call drawdowns based on unfunded commitment and upcoming investment pipeline. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Drawdown Scheduler

## Description
Schedules capital call drawdowns based on unfunded commitment and upcoming investment pipeline. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "drawdown_scheduler",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "drawdown_scheduler"`.
