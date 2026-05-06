---
skill: fee_drag_calculator
category: fund_admin
description: Estimates net IRR after management fees, performance carry, and other charges. Carry drag is only applied to returns above the hurdle rate.
tier: premium
inputs: none
---

# Fee Drag Calculator

## Description
Estimates net IRR after management fees, performance carry, and other charges. Carry drag is only applied to returns above the hurdle rate. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "fee_drag_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fee_drag_calculator"`.
