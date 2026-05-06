---
skill: portable_alpha_constructor
category: portfolio_construction
description: Combines capital allocations to uncorrelated alpha sleeves with a futures overlay sized to target beta exposure, following the portable alpha framework used by Canadian pensions.
tier: free
inputs: alpha_sleeves, beta_index, futures_spec
---

# Portable Alpha Constructor

## Description
Combines capital allocations to uncorrelated alpha sleeves with a futures overlay sized to target beta exposure, following the portable alpha framework used by Canadian pensions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `alpha_sleeves` | `array` | Yes | List of alpha sleeves including capital percentage and expected stats. |
| `beta_index` | `object` | Yes | Benchmark beta exposure stats (return, volatility). |
| `futures_spec` | `object` | Yes | Overlay futures specification (price, contract multiplier). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "portable_alpha_constructor",
  "arguments": {
    "alpha_sleeves": [],
    "beta_index": {},
    "futures_spec": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portable_alpha_constructor"`.
