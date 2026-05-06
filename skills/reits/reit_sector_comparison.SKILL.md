---
skill: reit_sector_comparison
category: reits
description: Benchmarks company metrics versus sector medians across KPIs.
tier: free
inputs: company_metrics, sector_medians
---

# Reit Sector Comparison

## Description
Benchmarks company metrics versus sector medians across KPIs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `company_metrics` | `object` | Yes |  |
| `sector_medians` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "reit_sector_comparison",
  "arguments": {
    "company_metrics": {},
    "sector_medians": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "reit_sector_comparison"`.
