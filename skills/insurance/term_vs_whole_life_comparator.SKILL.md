---
skill: term_vs_whole_life_comparator
category: insurance
description: Compare term vs whole life insurance. Calculates total cost of each and models investing the premium difference at a given return rate.
tier: free
inputs: coverage_amount, term_premium, whole_premium
---

# Term Vs Whole Life Comparator

## Description
Compare term vs whole life insurance. Calculates total cost of each and models investing the premium difference at a given return rate.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `coverage_amount` | `number` | Yes | Death benefit / coverage amount. |
| `term_years` | `integer` | No | Term policy length in years (default 20). |
| `term_premium` | `number` | Yes | Monthly term life premium. |
| `whole_premium` | `number` | Yes | Monthly whole life premium. |
| `investment_return` | `number` | No | Annual return rate on invested difference as decimal (default 0.07). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "term_vs_whole_life_comparator",
  "arguments": {
    "coverage_amount": 0,
    "term_premium": 0,
    "whole_premium": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "term_vs_whole_life_comparator"`.
