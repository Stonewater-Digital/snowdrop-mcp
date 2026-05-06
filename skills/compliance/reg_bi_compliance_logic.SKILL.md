---
skill: reg_bi_compliance_logic
category: compliance
description: Evaluates a broker-dealer recommendation against SEC Regulation Best Interest (17 CFR § 240.15l-1) four-obligation framework: Disclosure, Care, Conflict of Interest, and Compliance. Scores each obligation and identifies documentation requirements.
tier: premium
inputs: recommendation
---

# Reg Bi Compliance Logic

## Description
Evaluates a broker-dealer recommendation against SEC Regulation Best Interest (17 CFR § 240.15l-1) four-obligation framework: Disclosure, Care, Conflict of Interest, and Compliance. Scores each obligation and identifies documentation requirements. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `recommendation` | `object` | Yes | Broker-dealer recommendation details including security, customer profile, conflicts of interest disclosures, and supporting rationale for Reg BI obligation scoring |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "reg_bi_compliance_logic",
  "arguments": {
    "recommendation": {
      "security": "HIGH_YIELD_BOND_FUND",
      "customer_risk_tolerance": "moderate",
      "compensation_type": "commission",
      "conflicts_disclosed": true,
      "rationale": "Diversification benefit for fixed income allocation"
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "reg_bi_compliance_logic"`.
