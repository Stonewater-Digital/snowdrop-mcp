---
skill: utility_bill_analyzer
category: energy_finance
description: Analyze a series of monthly utility bills to find average cost per kWh, seasonal patterns, highest/lowest months, and overall trend.
tier: free
inputs: bills
---

# Utility Bill Analyzer

## Description
Analyze a series of monthly utility bills to find average cost per kWh, seasonal patterns, highest/lowest months, and overall trend.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `bills` | `array` | Yes | List of monthly bill records. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "utility_bill_analyzer",
  "arguments": {
    "bills": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "utility_bill_analyzer"`.
