---
skill: margin_requirement_calculator
category: fx
description: Calculate the margin required to open a forex position given position size and leverage. margin = position_size / leverage.
tier: free
inputs: position_size
---

# Margin Requirement Calculator

## Description
Calculate the margin required to open a forex position given position size and leverage. margin = position_size / leverage.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `position_size` | `number` | Yes | Total position size in account currency. |
| `leverage` | `number` | No | Leverage ratio (e.g. 50 for 50:1 leverage). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "margin_requirement_calculator",
  "arguments": {
    "position_size": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "margin_requirement_calculator"`.
