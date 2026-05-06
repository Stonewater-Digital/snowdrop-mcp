---
skill: compound_interest_calculator
category: personal_finance
description: Calculates the future value of an investment with compound interest, returning effective annual yield and year-by-year growth.
tier: free
inputs: principal, annual_rate, compounds_per_year, years
---

# Compound Interest Calculator

## Description
Calculates the future value of an investment with compound interest, returning effective annual yield and year-by-year growth.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `principal` | `number` | Yes | Initial amount invested in dollars, must be non-negative. |
| `annual_rate` | `number` | Yes | Nominal annual interest rate expressed as decimal (e.g., 0.05). |
| `compounds_per_year` | `number` | Yes | Number of compounding periods per year (1 for annual, 12 for monthly). |
| `years` | `number` | Yes | Investment horizon in years, can be fractional. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "compound_interest_calculator",
  "arguments": {
    "principal": 0,
    "annual_rate": 0,
    "compounds_per_year": 0,
    "years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "compound_interest_calculator"`.
