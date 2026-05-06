---
skill: debt_covenant_monitor
category: fund_accounting
description: Evaluates debt covenants against current financial ratios. Supports leverage_ratio (lower is better), interest_coverage (higher is better), and current_ratio (higher is better) covenant types.
tier: premium
inputs: covenants, financials
---

# Debt Covenant Monitor

## Description
Evaluates debt covenants against current financial ratios. Supports `leverage_ratio` (lower is better), `interest_coverage` (higher is better), and `current_ratio` (higher is better) covenant types. Returns breach status and distance-to-breach for each covenant. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `covenants` | `array` | Yes | List of covenant objects, each with `name`, `type` (e.g. `"leverage_ratio"`), and `threshold` value. |
| `financials` | `object` | Yes | Current financial snapshot with keys matching covenant types (e.g. `leverage_ratio`, `interest_coverage`, `current_ratio`). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "debt_covenant_monitor",
  "arguments": {
    "covenants": [
      {"name": "Senior Leverage", "type": "leverage_ratio", "threshold": 4.5},
      {"name": "Interest Coverage", "type": "interest_coverage", "threshold": 2.0},
      {"name": "Current Ratio", "type": "current_ratio", "threshold": 1.2}
    ],
    "financials": {
      "leverage_ratio": 3.8,
      "interest_coverage": 2.7,
      "current_ratio": 1.5,
      "total_debt": 45000000,
      "ebitda": 12000000
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "debt_covenant_monitor"`.
