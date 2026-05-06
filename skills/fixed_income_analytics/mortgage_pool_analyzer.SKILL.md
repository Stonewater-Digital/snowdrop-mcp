---
skill: mortgage_pool_analyzer
category: fixed_income_analytics
description: Calculates single-month mortality, conditional prepayment rate (CPR), conditional default rate (CDR), and loss severity for mortgage pools. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Mortgage Pool Analyzer

## Description
Calculates single-month mortality, conditional prepayment rate (CPR), conditional default rate (CDR), and loss severity for mortgage pools. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "mortgage_pool_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mortgage_pool_analyzer"`.
