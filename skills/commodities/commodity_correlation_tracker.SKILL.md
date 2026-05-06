---
skill: commodity_correlation_tracker
category: commodities
description: Computes pairwise Pearson correlations across commodity return series, identifies highest and lowest correlated pairs, and reports diversification score.
tier: free
inputs: returns_by_contract
---

# Commodity Correlation Tracker

## Description
Computes pairwise Pearson correlations across commodity return series, identifies highest and lowest correlated pairs, and reports diversification score.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns_by_contract` | `object` | Yes | Mapping of commodity name to its return series (decimal, same length). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "commodity_correlation_tracker",
  "arguments": {
    "returns_by_contract": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "commodity_correlation_tracker"`.
