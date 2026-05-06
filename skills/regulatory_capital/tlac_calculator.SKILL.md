---
skill: tlac_calculator
category: regulatory_capital
description: Calculates TLAC ratios vs 18% RWA and 6.75% leverage thresholds (US G-SIB).
tier: free
inputs: cet1, at1, tier2, eligible_senior, rwa, leverage_exposure
---

# Tlac Calculator

## Description
Calculates TLAC ratios vs 18% RWA and 6.75% leverage thresholds (US G-SIB).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cet1` | `number` | Yes | Common equity tier 1 |
| `at1` | `number` | Yes | Additional tier 1 capital |
| `tier2` | `number` | Yes | Tier 2 capital |
| `eligible_senior` | `number` | Yes | Eligible long-term debt |
| `rwa` | `number` | Yes | Risk-weighted assets |
| `leverage_exposure` | `number` | Yes | Total leverage exposure |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tlac_calculator",
  "arguments": {
    "cet1": 0,
    "at1": 0,
    "tier2": 0,
    "eligible_senior": 0,
    "rwa": 0,
    "leverage_exposure": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tlac_calculator"`.
