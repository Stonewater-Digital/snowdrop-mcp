---
skill: carried_interest_tax_analyzer
category: fund_tax
description: Calculates tax liability for carried interest under three-year rule. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Carried Interest Tax Analyzer

## Description
Calculates tax liability for carried interest under three-year rule. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "carried_interest_tax_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "carried_interest_tax_analyzer"`.
