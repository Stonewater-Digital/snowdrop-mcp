---
skill: borrower_credit_scorecard
category: private_credit
description: Generates weighted scorecard covering leverage, coverage, liquidity, and management.
tier: free
inputs: net_leverage, interest_coverage, liquidity_ratio, management_score
---

# Borrower Credit Scorecard

## Description
Generates weighted scorecard covering leverage, coverage, liquidity, and management.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_leverage` | `number` | Yes |  |
| `interest_coverage` | `number` | Yes |  |
| `liquidity_ratio` | `number` | Yes |  |
| `management_score` | `number` | Yes |  |
| `industry_outlook_score` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "borrower_credit_scorecard",
  "arguments": {
    "net_leverage": 0,
    "interest_coverage": 0,
    "liquidity_ratio": 0,
    "management_score": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "borrower_credit_scorecard"`.
