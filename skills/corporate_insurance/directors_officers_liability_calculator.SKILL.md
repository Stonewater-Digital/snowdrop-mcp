---
skill: directors_officers_liability_calculator
category: corporate_insurance
description: Estimates D&O expected loss, limit adequacy, and retention impacts.
tier: free
inputs: claim_frequency_pct, average_claim_severity, policy_limit, retention, market_cap
---

# Directors Officers Liability Calculator

## Description
Estimates D&O expected loss, limit adequacy, and retention impacts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `claim_frequency_pct` | `number` | Yes |  |
| `average_claim_severity` | `number` | Yes |  |
| `policy_limit` | `number` | Yes |  |
| `retention` | `number` | Yes |  |
| `market_cap` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "directors_officers_liability_calculator",
  "arguments": {
    "claim_frequency_pct": 0,
    "average_claim_severity": 0,
    "policy_limit": 0,
    "retention": 0,
    "market_cap": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "directors_officers_liability_calculator"`.
