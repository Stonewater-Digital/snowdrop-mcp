---
skill: tokenized_credit_portfolio_analyzer
category: rwa_tokenization
description: Aggregates RWA credit exposures to derive yield, expected loss, and coverage statistics.
tier: free
inputs: exposures
---

# Tokenized Credit Portfolio Analyzer

## Description
Aggregates RWA credit exposures to derive yield, expected loss, and coverage statistics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `exposures` | `array` | Yes | Per-loan details |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tokenized_credit_portfolio_analyzer",
  "arguments": {
    "exposures": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tokenized_credit_portfolio_analyzer"`.
