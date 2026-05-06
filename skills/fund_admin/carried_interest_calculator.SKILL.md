---
skill: carried_interest_calculator
category: fund_admin
description: Computes GP carried interest after returning LP capital and preferred return. Supports optional full GP catch-up tranche before profit split.
tier: premium
inputs: none
---

# Carried Interest Calculator

## Description
Computes GP carried interest after returning LP capital and preferred return. Supports optional full GP catch-up tranche before profit split. Uses European-style (whole-fund) waterfall logic. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "carried_interest_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "carried_interest_calculator"`.
