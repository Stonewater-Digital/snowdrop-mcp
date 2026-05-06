---
skill: loan_covenant_checker
category: credit_analysis
description: Tests financial covenants and highlights closest breaches.
tier: free
inputs: covenants, actuals
---

# Loan Covenant Checker

## Description
Tests financial covenants and highlights closest breaches.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `covenants` | `array` | Yes |  |
| `actuals` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "loan_covenant_checker",
  "arguments": {
    "covenants": [],
    "actuals": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "loan_covenant_checker"`.
