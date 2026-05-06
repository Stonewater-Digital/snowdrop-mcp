---
skill: commodity_term_structure_model
category: commodities
description: Fits an OLS linear regression to a commodity futures curve to estimate level (intercept at T=0), slope (price change per month), curvature (MSE of fit), and reports curve structure classification.
tier: free
inputs: futures_curve
---

# Commodity Term Structure Model

## Description
Fits an OLS linear regression to a commodity futures curve to estimate level (intercept at T=0), slope (price change per month), curvature (MSE of fit), and reports curve structure classification.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `futures_curve` | `array` | Yes | Futures curve points. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "commodity_term_structure_model",
  "arguments": {
    "futures_curve": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "commodity_term_structure_model"`.
