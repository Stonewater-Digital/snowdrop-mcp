---
skill: correlation_matrix_builder
category: risk
description: Build Pearson correlation matrices from asset price histories.
tier: free
inputs: price_series
---

# Correlation Matrix Builder

## Description
Build Pearson correlation matrices from asset price histories.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `price_series` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "correlation_matrix_builder",
  "arguments": {
    "price_series": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "correlation_matrix_builder"`.
