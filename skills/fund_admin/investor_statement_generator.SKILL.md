---
skill: investor_statement_generator
category: fund_admin
description: Builds LP investor statement data including NAV, DPI, TVPI, RVPI, unfunded commitment, and IRR. Validates that called capital does not exceed commitment.
tier: premium
inputs: none
---

# Investor Statement Generator

## Description
Builds LP investor statement data including NAV, DPI, TVPI, RVPI, unfunded commitment, and IRR. Validates that called capital does not exceed commitment. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "investor_statement_generator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "investor_statement_generator"`.
