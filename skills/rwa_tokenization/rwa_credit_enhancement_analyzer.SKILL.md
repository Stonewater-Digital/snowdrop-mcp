---
skill: rwa_credit_enhancement_analyzer
category: rwa_tokenization
description: Measures expected loss coverage from subordination, reserves, and insurance protections.
tier: free
inputs: pool_balance, expected_loss_pct, subordination_pct
---

# Rwa Credit Enhancement Analyzer

## Description
Measures expected loss coverage from subordination, reserves, and insurance protections.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pool_balance` | `number` | Yes | Outstanding asset pool balance |
| `expected_loss_pct` | `number` | Yes | Expected loss percent |
| `subordination_pct` | `number` | Yes | Junior tranche subordination percent |
| `reserve_pct` | `number` | No | Cash reserve percent |
| `insurance_pct` | `number` | No | Insurance coverage percent |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_credit_enhancement_analyzer",
  "arguments": {
    "pool_balance": 0,
    "expected_loss_pct": 0,
    "subordination_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_credit_enhancement_analyzer"`.
