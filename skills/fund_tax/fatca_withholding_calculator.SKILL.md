---
skill: fatca_withholding_calculator
category: fund_tax
description: Applies Chapter 4 withholding based on FATCA status and documentation validity. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Fatca Withholding Calculator

## Description
Applies Chapter 4 withholding based on FATCA status and documentation validity. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "fatca_withholding_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fatca_withholding_calculator"`.
