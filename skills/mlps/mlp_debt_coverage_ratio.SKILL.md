---
skill: mlp_debt_coverage_ratio
category: mlps
description: Computes EBITDA to debt service coverage for midstream partnerships. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Mlp Debt Coverage Ratio

## Description
Computes EBITDA to debt service coverage for midstream partnerships. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "mlp_debt_coverage_ratio",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mlp_debt_coverage_ratio"`.
