---
skill: rwa_real_estate_environmental_report_checker
category: crypto_rwa
description: Validates environmental assessments and ensures mitigation steps are recorded on-chain.
tier: free
inputs: payload
---

# Rwa Real Estate Environmental Report Checker

## Description
Validates environmental assessments and ensures mitigation steps are recorded on-chain.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_real_estate_environmental_report_checker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_environmental_report_checker"`.
