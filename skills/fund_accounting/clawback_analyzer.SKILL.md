---
skill: clawback_analyzer
category: fund_accounting
description: Determines whether the GP owes a clawback based on carry received versus carry entitled after preferred return. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: total_distributions, total_contributions, preferred_return, carry_received, carry_rate
---

# Clawback Analyzer

## Description
Determines whether the GP owes a clawback based on carry received versus carry entitled after preferred return. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_distributions` | `number` | Yes | Total cash distributions made to LPs over the fund's life in dollars. |
| `total_contributions` | `number` | Yes | Total LP capital contributions made into the fund in dollars. |
| `preferred_return` | `number` | Yes | Preferred return amount (dollar value) owed to LPs before GP carry is earned. |
| `carry_received` | `number` | Yes | Total carried interest already distributed to the GP in dollars. |
| `carry_rate` | `number` | No | GP carried interest rate (e.g. `0.20` for 20%). Defaults to `0.20`. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "clawback_analyzer",
  "arguments": {
    "total_distributions": 85000000,
    "total_contributions": 50000000,
    "preferred_return": 4000000,
    "carry_received": 7500000,
    "carry_rate": 0.20
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "clawback_analyzer"`.
