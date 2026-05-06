---
skill: lp_reporting_standard
category: fund_accounting
description: Generates an ILPA (Institutional Limited Partners Association) compliant quarterly fund report in markdown format. Validates presence of all required ILPA Reporting Template v2 fields and flags any that are missing or null.
tier: premium
inputs: none
---

# Lp Reporting Standard

## Description
Generates an ILPA (Institutional Limited Partners Association) compliant quarterly fund report in markdown format. Validates presence of all required ILPA Reporting Template v2 fields and flags any that are missing or null. Produces structured markdown with sections for Fund Overview, Performance Metrics, Top Holdings, Cash Position, and Upcoming Events. (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "lp_reporting_standard",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "lp_reporting_standard"`.
