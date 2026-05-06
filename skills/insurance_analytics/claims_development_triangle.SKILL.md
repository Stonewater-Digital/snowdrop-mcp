---
skill: claims_development_triangle
category: insurance_analytics
description: Constructs a cumulative loss development triangle and computes volume-weighted age-to-age factors, tail factor, and cumulative-to-ultimate factors from a list of claim records with accident_year, development_year, and cumulative_paid fields.
tier: free
inputs: claims
---

# Claims Development Triangle

## Description
Constructs a cumulative loss development triangle and computes volume-weighted age-to-age factors, tail factor, and cumulative-to-ultimate factors from a list of claim records with accident_year, development_year, and cumulative_paid fields.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `claims` | `array` | Yes | List of claim records. Each record must include: accident_year (int), development_year (int, 1-indexed), and cumulative_paid (number >= 0). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "claims_development_triangle",
  "arguments": {
    "claims": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "claims_development_triangle"`.
