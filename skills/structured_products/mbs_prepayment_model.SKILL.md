---
skill: mbs_prepayment_model
category: structured_products
description: Generates PSA-based CPR and SMM projections plus collateral amortization and balance run-off stats. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Mbs Prepayment Model

## Description
Generates PSA-based CPR and SMM projections plus collateral amortization and balance run-off stats. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "mbs_prepayment_model",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mbs_prepayment_model"`.
