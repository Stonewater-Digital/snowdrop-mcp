---
skill: vendor_due_diligence
category: vendor_eval
description: Scores vendor fit based on uptime, pricing, certifications, and experience.
tier: free
inputs: vendor, requirements
---

# Vendor Due Diligence

## Description
Scores vendor fit based on uptime, pricing, certifications, and experience.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `vendor` | `object` | Yes | Vendor profile with fields: `name` (string), `uptime_pct` (float), `monthly_cost_usd` (float), `certifications` (array of strings), and `years_experience` (int). |
| `requirements` | `object` | Yes | Evaluation thresholds: `min_uptime_pct` (float), `max_monthly_cost_usd` (float), `required_certifications` (array of strings), `min_years_experience` (int). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "vendor_due_diligence",
  "arguments": {
    "vendor": {
      "name": "DataBridge Inc",
      "uptime_pct": 99.7,
      "monthly_cost_usd": 450,
      "certifications": ["SOC2", "ISO27001"],
      "years_experience": 8
    },
    "requirements": {
      "min_uptime_pct": 99.5,
      "max_monthly_cost_usd": 500,
      "required_certifications": ["SOC2"],
      "min_years_experience": 3
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vendor_due_diligence"`.
