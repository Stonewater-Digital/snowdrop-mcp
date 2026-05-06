---
skill: capital_call_calculator
category: fund_admin
description: Calculates LP capital call wire amounts based on commitment percentages. Supports per-call fund expenses and validates that call_pct does not exceed remaining unfunded commitment.
tier: premium
inputs: lp_commitments, call_pct, fees_pct
---

# Capital Call Calculator

## Description
Calculates LP capital call wire amounts based on commitment percentages. Supports per-call fund expenses and validates that call_pct does not exceed remaining unfunded commitment. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| lp_commitments | array | Yes | List of LP objects, each with `lp_name` (string), `commitment` (number), and `called` (number) representing total commitment and previously called capital |
| call_pct | number | Yes | Percentage of each LP's total commitment to call in this notice (e.g. 15.0 for 15%) |
| fees_pct | number | No | Additional fund expense percentage layered on top of the investment call (default: 0.0) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "capital_call_calculator",
  "arguments": {
    "lp_commitments": [
      {"lp_name": "State Teachers Pension Fund", "commitment": 20000000, "called": 6000000},
      {"lp_name": "University Endowment Trust", "commitment": 10000000, "called": 3000000},
      {"lp_name": "Sovereign Wealth Co-Invest", "commitment": 5000000, "called": 1500000}
    ],
    "call_pct": 15.0,
    "fees_pct": 0.5
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "capital_call_calculator"`.
