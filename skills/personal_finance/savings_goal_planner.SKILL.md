---
skill: savings_goal_planner
category: personal_finance
description: Solves for the monthly contribution required to hit a savings goal given current balance, time horizon, and expected return, with annual milestones.
tier: free
inputs: target_amount, current_savings, annual_rate, years
---

# Savings Goal Planner

## Description
Solves for the monthly contribution required to hit a savings goal given current balance, time horizon, and expected return, with annual milestones.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `target_amount` | `number` | Yes | Desired ending balance in dollars, must exceed zero. |
| `current_savings` | `number` | Yes | Existing savings earmarked for the goal, non-negative dollars. |
| `annual_rate` | `number` | Yes | Expected annual return as decimal (can be zero or negative). |
| `years` | `number` | Yes | Years until goal, can be fractional but must be positive. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "savings_goal_planner",
  "arguments": {
    "target_amount": 0,
    "current_savings": 0,
    "annual_rate": 0,
    "years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "savings_goal_planner"`.
