---
skill: cds_index_portfolio_analyzer
category: credit_default_swaps
description: Aggregates CDS index notionals, sectors, and risk skew.
tier: free
inputs: positions
---

# Cds Index Portfolio Analyzer

## Description
Aggregates CDS index notionals, sectors, and risk skew.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_index_portfolio_analyzer",
  "arguments": {
    "positions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_index_portfolio_analyzer"`.
