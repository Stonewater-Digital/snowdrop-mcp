---
skill: apy_to_apr_converter
category: banking
description: Convert Annual Percentage Yield (APY) to Annual Percentage Rate (APR) given compounding frequency. APR = n * ((1 + APY)^(1/n) - 1).
tier: free
inputs: apy
---

# Apy To Apr Converter

## Description
Convert Annual Percentage Yield (APY) to Annual Percentage Rate (APR) given compounding frequency. APR = n * ((1 + APY)^(1/n) - 1).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `apy` | `number` | Yes | Annual Percentage Yield as a decimal (e.g., 0.05 for 5%). |
| `compounds_per_year` | `integer` | No | Number of compounding periods per year (default 12 for monthly). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "apy_to_apr_converter",
  "arguments": {
    "apy": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "apy_to_apr_converter"`.
