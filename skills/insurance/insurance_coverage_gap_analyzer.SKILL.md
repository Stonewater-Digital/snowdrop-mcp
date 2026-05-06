---
skill: insurance_coverage_gap_analyzer
category: insurance
description: Analyze insurance coverage gaps across life, disability, and health categories. Provides per-category gap analysis and an overall protection score.
tier: free
inputs: total_assets, total_liabilities, current_life, current_disability, current_health_oop_max
---

# Insurance Coverage Gap Analyzer

## Description
Analyze insurance coverage gaps across life, disability, and health categories. Provides per-category gap analysis and an overall protection score.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_assets` | `number` | Yes | Total assets / net worth. |
| `total_liabilities` | `number` | Yes | Total outstanding liabilities. |
| `current_life` | `number` | Yes | Current life insurance coverage. |
| `current_disability` | `number` | Yes | Current monthly disability benefit. |
| `current_health_oop_max` | `number` | Yes | Current health plan out-of-pocket maximum. |
| `dependents` | `integer` | No | Number of dependents (default 0). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "insurance_coverage_gap_analyzer",
  "arguments": {
    "total_assets": 0,
    "total_liabilities": 0,
    "current_life": 0,
    "current_disability": 0,
    "current_health_oop_max": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "insurance_coverage_gap_analyzer"`.
