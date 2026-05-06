---
skill: calc_waterfall_dist
category: fund_accounting
description: Calculates LP/GP waterfall distributions across preferred return, catch-up, and carried interest tiers. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Calc Waterfall Dist

## Description
Calculates LP/GP waterfall distributions across preferred return, catch-up, and carried interest tiers. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "calc_waterfall_dist",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "calc_waterfall_dist"`.
