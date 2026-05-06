---
skill: foreign_tax_credit_calculator
category: fund_tax
description: Applies the FTC limitation formula for passive and general baskets. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Foreign Tax Credit Calculator

## Description
Applies the FTC limitation formula for passive and general baskets. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "foreign_tax_credit_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "foreign_tax_credit_calculator"`.
