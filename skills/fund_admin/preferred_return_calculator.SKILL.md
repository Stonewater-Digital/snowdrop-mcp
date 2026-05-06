---
skill: preferred_return_calculator
category: fund_admin
description: Calculates accrued preferred return on LP capital with configurable compounding frequency. Supports annual, quarterly, monthly, and daily compounding.
tier: premium
inputs: none
---

# Preferred Return Calculator

## Description
Calculates accrued preferred return on LP capital with configurable compounding frequency. Supports annual, quarterly, monthly, and daily compounding. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "preferred_return_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "preferred_return_calculator"`.
