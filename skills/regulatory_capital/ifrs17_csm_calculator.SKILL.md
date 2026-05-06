---
skill: ifrs17_csm_calculator
category: regulatory_capital
description: Calculates IFRS 17 contractual service margin and amortizes it over coverage units.
tier: free
inputs: fulfillment_cashflows, risk_adjustment, premium_received, discount_rate_pct, coverage_units
---

# Ifrs17 Csm Calculator

## Description
Calculates IFRS 17 contractual service margin and amortizes it over coverage units.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fulfillment_cashflows` | `array` | Yes | Expected future cashflows with timing in years. |
| `risk_adjustment` | `number` | Yes | Risk adjustment amount. |
| `premium_received` | `number` | Yes | Premium received at inception. |
| `discount_rate_pct` | `number` | Yes | Discount rate for PV. |
| `coverage_units` | `array` | Yes | Coverage units per period for CSM release. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ifrs17_csm_calculator",
  "arguments": {
    "fulfillment_cashflows": [],
    "risk_adjustment": 0,
    "premium_received": 0,
    "discount_rate_pct": 0,
    "coverage_units": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ifrs17_csm_calculator"`.
