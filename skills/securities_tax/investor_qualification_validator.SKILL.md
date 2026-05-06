---
skill: investor_qualification_validator
category: securities_tax
description: Validates accredited investor status using income and net worth thresholds.
tier: free
inputs: net_worth, annual_income
---

# Investor Qualification Validator

## Description
Validates accredited investor status using income and net worth thresholds.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_worth` | `number` | Yes |  |
| `annual_income` | `number` | Yes |  |
| `joint` | `boolean` | No |  |
| `professional_certifications` | `boolean` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "investor_qualification_validator",
  "arguments": {
    "net_worth": 0,
    "annual_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "investor_qualification_validator"`.
