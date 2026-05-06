---
skill: reit_dividend_coverage
category: real_estate
description: Evaluates REIT dividend sustainability by computing FFO and AFFO payout coverage ratios. Classifies risk as low, medium, or high, and flags dividends at risk of cuts.
tier: free
inputs: ffo, dividends_paid
---

# Reit Dividend Coverage

## Description
Evaluates REIT dividend sustainability by computing FFO and AFFO payout coverage ratios. Classifies risk as low, medium, or high, and flags dividends at risk of cuts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ffo` | `number` | Yes | Funds From Operations for the period (dollars). |
| `dividends_paid` | `number` | Yes | Total dividends paid to shareholders for the period (dollars). |
| `affo` | `number` | No | Adjusted FFO for the period (optional, dollars). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "reit_dividend_coverage",
  "arguments": {
    "ffo": 0,
    "dividends_paid": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "reit_dividend_coverage"`.
