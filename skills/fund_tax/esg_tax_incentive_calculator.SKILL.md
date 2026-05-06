---
skill: esg_tax_incentive_calculator
category: fund_tax
description: Models ESG incentives including IRC §§45/48 credits, Canada's Clean Technology ITC, and the Dutch EIA regime. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Esg Tax Incentive Calculator

## Description
Models ESG incentives including IRC §§45/48 credits, Canada's Clean Technology ITC, and the Dutch EIA regime. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "esg_tax_incentive_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "esg_tax_incentive_calculator"`.
