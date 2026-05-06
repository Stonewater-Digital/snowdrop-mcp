---
skill: apr_to_apy_converter
category: banking
description: Convert Annual Percentage Rate (APR) to Annual Percentage Yield (APY) given compounding frequency. APY = (1 + APR/n)^n - 1.
tier: free
inputs: apr
---

# Apr To Apy Converter

## Description
Convert Annual Percentage Rate (APR) to Annual Percentage Yield (APY) given compounding frequency. APY = (1 + APR/n)^n - 1.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `apr` | `number` | Yes | Annual Percentage Rate as a decimal (e.g., 0.05 for 5%). |
| `compounds_per_year` | `integer` | No | Number of compounding periods per year (default 12 for monthly). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "apr_to_apy_converter",
  "arguments": {
    "apr": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "apr_to_apy_converter"`.
