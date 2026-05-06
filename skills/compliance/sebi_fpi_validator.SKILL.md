---
skill: sebi_fpi_validator
category: compliance
description: Validates Foreign Portfolio Investor (FPI) compliance under SEBI (Foreign Portfolio Investors) Regulations, 2019. Determines FPI Category I, II, or III; checks the 10% single-company investment limit, 24%/49% sectoral caps, and grandfathering provisions.
tier: premium
inputs: entity_data
---

# Sebi Fpi Validator

## Description
Validates Foreign Portfolio Investor (FPI) compliance under SEBI (Foreign Portfolio Investors) Regulations, 2019. Determines FPI Category I, II, or III; checks the 10% single-company investment limit, 24%/49% sectoral caps, and grandfathering provisions. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `entity_data` | `object` | Yes | FPI entity details including investor type, home jurisdiction, AUM, portfolio holdings, and single-company/sectoral investment percentages for SEBI FPI Regulations 2019 validation |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sebi_fpi_validator",
  "arguments": {
    "entity_data": {
      "investor_type": "sovereign_wealth_fund",
      "home_jurisdiction": "SG",
      "aum_usd": 5000000000,
      "single_company_pct": 8.5,
      "sector": "IT"
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sebi_fpi_validator"`.
