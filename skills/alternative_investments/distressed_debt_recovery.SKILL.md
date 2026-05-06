---
skill: distressed_debt_recovery
category: alternative_investments
description: Waterfalls enterprise value through senior/mezz/equity to compute recoveries and implied returns. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Distressed Debt Recovery

## Description
Waterfalls enterprise value through senior/mezz/equity to compute recoveries and implied returns. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "distressed_debt_recovery",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "distressed_debt_recovery"`.
