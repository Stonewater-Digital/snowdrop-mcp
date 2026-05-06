---
skill: recallable_distribution_tracker
category: fund_admin
description: Summarizes recallable vs permanent distributions per LP. Recallable distributions can be called back by the GP for follow-on investments.
tier: premium
inputs: none
---

# Recallable Distribution Tracker

## Description
Summarizes recallable vs permanent distributions per LP. Recallable distributions can be called back by the GP for follow-on investments. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "recallable_distribution_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "recallable_distribution_tracker"`.
