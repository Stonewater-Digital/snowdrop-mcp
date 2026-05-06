---
skill: cpi_inflation_calculator
category: public_data
description: Calculate inflation-adjusted values using CPI data. Uses hardcoded CPI table (2015-2025) with optional BLS API lookup when BLS_API_KEY is set.
tier: free
inputs: start_year, start_month, end_year, end_month
---

# Cpi Inflation Calculator

## Description
Calculate inflation-adjusted values using CPI data. Uses hardcoded CPI table (2015-2025) with optional BLS API lookup when BLS_API_KEY is set.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `start_year` | `integer` | Yes | Starting year (2015-2025). |
| `start_month` | `integer` | Yes | Starting month (1-12). |
| `end_year` | `integer` | Yes | Ending year (2015-2025). |
| `end_month` | `integer` | Yes | Ending month (1-12). |
| `amount` | `number` | No | Dollar amount to adjust for inflation. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cpi_inflation_calculator",
  "arguments": {
    "start_year": 0,
    "start_month": 0,
    "end_year": 0,
    "end_month": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cpi_inflation_calculator"`.
