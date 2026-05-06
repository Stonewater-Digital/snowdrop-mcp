---
skill: pfic_qef_calculator
category: fund_tax
description: Calculates PFIC inclusions and §1291 interest adjustments for offshore funds. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Pfic Qef Calculator

## Description
Calculates PFIC inclusions and §1291 interest adjustments for offshore funds. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "pfic_qef_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pfic_qef_calculator"`.
