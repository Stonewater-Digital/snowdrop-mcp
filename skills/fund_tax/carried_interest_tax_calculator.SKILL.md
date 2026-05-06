---
skill: carried_interest_tax_calculator
category: fund_tax
description: Recharacterizes carried interest under IRC §1061's three-year holding period rule. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Carried Interest Tax Calculator

## Description
Recharacterizes carried interest under IRC §1061's three-year holding period rule. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "carried_interest_tax_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "carried_interest_tax_calculator"`.
