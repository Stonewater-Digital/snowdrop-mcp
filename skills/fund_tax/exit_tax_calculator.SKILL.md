---
skill: exit_tax_calculator
category: fund_tax
description: Computes exit tax exposures for investors emigrating from the US, Germany, or Canada. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Exit Tax Calculator

## Description
Computes exit tax exposures for investors emigrating from the US, Germany, or Canada. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "exit_tax_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "exit_tax_calculator"`.
