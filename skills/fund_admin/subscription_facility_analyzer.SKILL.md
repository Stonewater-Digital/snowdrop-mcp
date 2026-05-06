---
skill: subscription_facility_analyzer
category: fund_admin
description: Evaluates subscription credit facility utilization, annualized interest cost, unused fee drag, and NAV impact. Subscription lines are backed by LP commitments.
tier: premium
inputs: facility_limit, drawn_amount, spread_bps, nav, base_rate_pct, unused_fee_bps
---

# Subscription Facility Analyzer

## Description
Evaluates subscription credit facility utilization, annualized interest cost, unused fee drag, and NAV impact. Subscription lines are backed by LP commitments. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| facility_limit | number | Yes | Maximum borrowing capacity of the subscription credit facility (USD) |
| drawn_amount | number | Yes | Current outstanding balance drawn on the subscription facility (USD) |
| spread_bps | number | Yes | Lender spread over the base rate in basis points (e.g. 175 for 1.75%) |
| nav | number | Yes | Fund net asset value used to express interest cost as a percentage drag on returns (USD) |
| base_rate_pct | number | No | Base reference rate (e.g. SOFR) as a percentage (default: 0.0) |
| unused_fee_bps | number | No | Commitment fee on the undrawn portion of the facility in basis points (default: 50.0) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "subscription_facility_analyzer",
  "arguments": {
    "facility_limit": 30000000,
    "drawn_amount": 18000000,
    "spread_bps": 175,
    "nav": 95000000,
    "base_rate_pct": 5.33,
    "unused_fee_bps": 50.0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "subscription_facility_analyzer"`.
