---
skill: correlation_matrix_builder
category: quant
description: Generates pairwise correlation matrix and summary statistics.
tier: free
inputs: returns_by_asset
---

# Correlation Matrix Builder

## Description
Generates pairwise correlation matrix and summary statistics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns_by_asset` | `object` | Yes |  |

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
    "returns_by_asset": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "correlation_matrix_builder"`.
