---
skill: cmo_cashflow_waterfall
category: structured_products
description: Projects mortgage collateral cashflows with PSA prepayments and allocates them through sequential/PAC/TAC tranches to report WALs and yields. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Cmo Cashflow Waterfall

## Description
Projects mortgage collateral cashflows with PSA prepayments and allocates them through sequential/PAC/TAC tranches to report WALs and yields. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "cmo_cashflow_waterfall",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cmo_cashflow_waterfall"`.
