---
skill: j_curve_analyzer
category: fund_admin
description: Builds cumulative net cash flow timeline highlighting J-curve characteristics: trough depth, trough year, recovery year (breakeven), and total net return. Negative early net flows create the characteristic J shape.
tier: premium
inputs: periods
---

# J Curve Analyzer

## Description
Builds cumulative net cash flow timeline highlighting J-curve characteristics: trough depth, trough year, recovery year (breakeven), and total net return. Negative early net flows create the characteristic J shape. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| periods | array | Yes | Ordered list of period objects, each with `year` (number), `contributions` (number), and `distributions` (number) representing annual fund cash flow activity |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "j_curve_analyzer",
  "arguments": {
    "periods": [
      {"year": 1, "contributions": 12000000, "distributions": 0},
      {"year": 2, "contributions": 18000000, "distributions": 500000},
      {"year": 3, "contributions": 10000000, "distributions": 2000000},
      {"year": 4, "contributions": 5000000, "distributions": 8000000},
      {"year": 5, "contributions": 0, "distributions": 22000000},
      {"year": 6, "contributions": 0, "distributions": 35000000}
    ]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "j_curve_analyzer"`.
