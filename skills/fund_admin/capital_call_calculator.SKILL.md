---
skill: capital_call_calculator
category: fund_admin
description: Calculates LP capital call wire amounts based on commitment percentages. Supports per-call fund expenses and validates that call_pct does not exceed remaining unfunded commitment.
tier: premium
inputs: none
---

# Capital Call Calculator

## Description
Calculates LP capital call wire amounts based on commitment percentages. Supports per-call fund expenses and validates that call_pct does not exceed remaining unfunded commitment. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "capital_call_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "capital_call_calculator"`.
