---
skill: j_curve_modeler
category: fund_accounting
description: Simulates fund cash flows, NAV, and J-curve inflection metrics. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# J Curve Modeler

## Description
Simulates fund cash flows, NAV, and J-curve inflection metrics. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "j_curve_modeler",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "j_curve_modeler"`.
