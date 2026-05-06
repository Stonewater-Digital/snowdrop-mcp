---
skill: credit_age_calculator
category: credit
description: Calculate average, oldest, and newest credit account ages from a list of ISO-format account open dates.
tier: free
inputs: account_open_dates
---

# Credit Age Calculator

## Description
Calculate average, oldest, and newest credit account ages from a list of ISO-format account open dates.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `account_open_dates` | `array` | Yes | List of account open dates in ISO format (YYYY-MM-DD). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_age_calculator",
  "arguments": {
    "account_open_dates": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_age_calculator"`.
