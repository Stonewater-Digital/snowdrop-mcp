---
skill: rebalance_trigger
category: fund_accounting
description: Checks portfolio split vs. target bands and surfaces recommended skims or reviews.
tier: premium
inputs: none
---

# Rebalance Trigger

## Description
Checks portfolio split vs. target bands and surfaces recommended skims or reviews. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "rebalance_trigger",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rebalance_trigger"`.
