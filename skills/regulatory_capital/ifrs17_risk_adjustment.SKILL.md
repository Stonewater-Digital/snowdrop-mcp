---
skill: ifrs17_risk_adjustment
category: regulatory_capital
description: Computes risk adjustment as VaR minus expected loss using the confidence level technique.
tier: free
inputs: claim_distribution, confidence_level, coefficient_of_variation_pct
---

# Ifrs17 Risk Adjustment

## Description
Computes risk adjustment as VaR minus expected loss using the confidence level technique.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `claim_distribution` | `array` | Yes | Simulated claim amounts or scenario losses. |
| `confidence_level` | `number` | Yes | Target confidence level (e.g., 0.75). |
| `coefficient_of_variation_pct` | `number` | Yes | Coefficient of variation per risk type. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ifrs17_risk_adjustment",
  "arguments": {
    "claim_distribution": [],
    "confidence_level": 0,
    "coefficient_of_variation_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ifrs17_risk_adjustment"`.
