---
skill: cre_cap_rate_aggregator
category: real_estate
description: Aggregates capitalization rates from a list of comparable CRE sales. Computes individual cap rates (NOI / sale_price), then averages by asset class (office, retail, multifamily, etc.) and by market (MSA).
tier: free
inputs: comparables
---

# Cre Cap Rate Aggregator

## Description
Aggregates capitalization rates from a list of comparable CRE sales. Computes individual cap rates (NOI / sale_price), then averages by asset class (office, retail, multifamily, etc.) and by market (MSA). Returns overall market average and outlier flags.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `comparables` | `array` | Yes | List of comparable sales. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cre_cap_rate_aggregator",
  "arguments": {
    "comparables": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cre_cap_rate_aggregator"`.
