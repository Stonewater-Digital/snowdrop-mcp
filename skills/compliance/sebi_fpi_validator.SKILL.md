---
skill: sebi_fpi_validator
category: compliance
description: Validates Foreign Portfolio Investor (FPI) compliance under SEBI (Foreign Portfolio Investors) Regulations, 2019. Determines FPI Category I, II, or III; checks the 10% single-company investment limit, 24%/49% sectoral caps, and grandfathering provisions.
tier: premium
inputs: none
---

# Sebi Fpi Validator

## Description
Validates Foreign Portfolio Investor (FPI) compliance under SEBI (Foreign Portfolio Investors) Regulations, 2019. Determines FPI Category I, II, or III; checks the 10% single-company investment limit, 24%/49% sectoral caps, and grandfathering provisions. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "sebi_fpi_validator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sebi_fpi_validator"`.
