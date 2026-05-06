---
skill: distribution_waterfall_modeler
category: fund_accounting
description: Calculates LP/GP outcomes for American and European waterfalls with tier detail. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Distribution Waterfall Modeler

## Description
Calculates LP/GP outcomes for American and European waterfalls with tier detail. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "distribution_waterfall_modeler",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "distribution_waterfall_modeler"`.
