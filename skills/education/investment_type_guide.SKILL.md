---
skill: investment_type_guide
category: education
description: Returns overview of major investment types (stocks, bonds, mutual funds, ETFs, real estate, commodities) with risk/return profiles.
tier: free
inputs: none
---

# Investment Type Guide

## Description
Returns overview of major investment types (stocks, bonds, mutual funds, ETFs, real estate, commodities) with risk/return profiles.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `investment_type` | `string` | No | Optional specific investment type to look up. If omitted, returns all types. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "investment_type_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "investment_type_guide"`.
