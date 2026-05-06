---
skill: skewness_kurtosis_analyzer
category: market_analytics
description: Computes skewness, kurtosis, and Jarque-Bera statistic for return distributions.
tier: free
inputs: returns
---

# Skewness Kurtosis Analyzer

## Description
Computes skewness, kurtosis, and Jarque-Bera statistic for return distributions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | Return series. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "skewness_kurtosis_analyzer",
  "arguments": {
    "returns": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skewness_kurtosis_analyzer"`.
