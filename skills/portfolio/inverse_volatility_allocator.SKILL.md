---
skill: inverse_volatility_allocator
category: portfolio
description: Allocates a portfolio using inverse-volatility weighting, giving more weight to lower-volatility assets.
tier: free
inputs: volatilities
---

# Inverse Volatility Allocator

## Description
Allocates a portfolio using inverse-volatility weighting, giving more weight to lower-volatility assets.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `volatilities` | `array` | Yes | List of asset volatilities (must all be > 0). |
| `total_value` | `number` | No | Total portfolio value to allocate (default 10000). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "inverse_volatility_allocator",
  "arguments": {
    "volatilities": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "inverse_volatility_allocator"`.
