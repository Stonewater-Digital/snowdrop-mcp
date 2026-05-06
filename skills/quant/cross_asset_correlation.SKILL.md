---
skill: cross_asset_correlation
category: quant
description: Computes pairwise correlations across asset classes and flags concentration risks.
tier: free
inputs: asset_class_returns
---

# Cross Asset Correlation

## Description
Computes pairwise correlations across asset classes and flags concentration risks.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset_class_returns` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cross_asset_correlation",
  "arguments": {
    "asset_class_returns": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cross_asset_correlation"`.
