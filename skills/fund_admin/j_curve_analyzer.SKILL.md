---
skill: j_curve_analyzer
category: fund_admin
description: Builds cumulative net cash flow timeline highlighting J-curve characteristics: trough depth, trough year, recovery year (breakeven), and total net return. Negative early net flows create the characteristic J shape.
tier: premium
inputs: none
---

# J Curve Analyzer

## Description
Builds cumulative net cash flow timeline highlighting J-curve characteristics: trough depth, trough year, recovery year (breakeven), and total net return. Negative early net flows create the characteristic J shape. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "j_curve_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "j_curve_analyzer"`.
