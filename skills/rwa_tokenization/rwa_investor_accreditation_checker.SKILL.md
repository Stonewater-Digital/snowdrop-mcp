---
skill: rwa_investor_accreditation_checker
category: rwa_tokenization
description: Evaluates investor profile against configurable accreditation thresholds.
tier: free
inputs: annual_income, net_worth
---

# Rwa Investor Accreditation Checker

## Description
Evaluates investor profile against configurable accreditation thresholds.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_income` | `number` | Yes | Investor annual income |
| `net_worth` | `number` | Yes | Investor net worth |
| `min_income_threshold` | `number` | No | Income threshold |
| `min_net_worth_threshold` | `number` | No | Net worth threshold |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_investor_accreditation_checker",
  "arguments": {
    "annual_income": 0,
    "net_worth": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_investor_accreditation_checker"`.
