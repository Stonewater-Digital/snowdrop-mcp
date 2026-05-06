---
skill: cds_correlation_basket_analyzer
category: credit_default_swaps
description: Analyzes basket correlation scenarios and tranche loss contributions.
tier: free
inputs: exposures, base_correlation, attachment_points_pct, detachment_points_pct
---

# Cds Correlation Basket Analyzer

## Description
Analyzes basket correlation scenarios and tranche loss contributions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `exposures` | `array` | Yes |  |
| `base_correlation` | `number` | Yes |  |
| `attachment_points_pct` | `array` | Yes |  |
| `detachment_points_pct` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_correlation_basket_analyzer",
  "arguments": {
    "exposures": [],
    "base_correlation": 0,
    "attachment_points_pct": [],
    "detachment_points_pct": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_correlation_basket_analyzer"`.
