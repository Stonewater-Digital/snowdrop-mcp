---
skill: employer_401k_match_optimizer
category: personal_finance
description: Evaluates contribution rates needed to earn the full employer match while respecting IRS limits and highlights remaining match dollars on the table.
tier: free
inputs: salary, employer_match_pct, employer_match_cap_pct, current_contribution_pct, annual_limit
---

# Employer 401k Match Optimizer

## Description
Evaluates contribution rates needed to earn the full employer match while respecting IRS limits and highlights remaining match dollars on the table.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `salary` | `number` | Yes | Gross annual salary eligible for the 401(k) plan. |
| `employer_match_pct` | `number` | Yes | Employer match percentage (e.g., 0.5 for 50% match). |
| `employer_match_cap_pct` | `number` | Yes | Maximum salary percentage the employer will match. |
| `current_contribution_pct` | `number` | Yes | Employee's current contribution percentage of salary. |
| `annual_limit` | `number` | Yes | IRS annual contribution limit in dollars. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "employer_401k_match_optimizer",
  "arguments": {
    "salary": 0,
    "employer_match_pct": 0,
    "employer_match_cap_pct": 0,
    "current_contribution_pct": 0,
    "annual_limit": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "employer_401k_match_optimizer"`.
