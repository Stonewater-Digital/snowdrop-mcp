---
skill: earnings_quality_analyzer
category: public_finance
description: Computes accrual ratios, Beneish M-Score, and manipulation risk.
tier: free
inputs: financials
---

# Earnings Quality Analyzer

## Description
Computes accrual ratios, Beneish M-Score, and manipulation risk.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `financials` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "earnings_quality_analyzer",
  "arguments": {
    "financials": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "earnings_quality_analyzer"`.
