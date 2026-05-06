---
skill: cd_ladder_builder
category: personal_finance
description: Constructs a certificate-of-deposit ladder by distributing capital across available terms, reporting allocation, weighted yield, and liquidity schedule.
tier: free
inputs: total_investment, cd_terms_available, ladder_rungs
---

# Cd Ladder Builder

## Description
Constructs a certificate-of-deposit ladder by distributing capital across available terms, reporting allocation, weighted yield, and liquidity schedule.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_investment` | `number` | Yes | Dollars available to invest, must be positive. |
| `cd_terms_available` | `array` | Yes | List of term options with months and APY values. |
| `ladder_rungs` | `number` | Yes | Desired number of ladder positions (e.g., 4 for quarterly). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cd_ladder_builder",
  "arguments": {
    "total_investment": 0,
    "cd_terms_available": [],
    "ladder_rungs": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cd_ladder_builder"`.
