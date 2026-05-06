---
skill: cds_basis_trade_analyzer
category: credit_derivatives
description: Decomposes the CDS-cash basis into coupon, financing, and default-leg components using basis trading conventions (Hull, Ch. 24).
tier: free
inputs: cash_spread_bp, cds_spread_bp, repo_rate_bp, funding_rate_bp, expected_loss_bp
---

# Cds Basis Trade Analyzer

## Description
Decomposes the CDS-cash basis into coupon, financing, and default-leg components using basis trading conventions (Hull, Ch. 24).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cash_spread_bp` | `number` | Yes | Asset-swap or bond spread in basis points of yield. |
| `cds_spread_bp` | `number` | Yes | Quoted CDS running spread in basis points. |
| `repo_rate_bp` | `number` | Yes | Term repo rate used to finance the bond, in basis points. |
| `funding_rate_bp` | `number` | Yes | Dealer funding curve rate for the same maturity, in basis points. |
| `expected_loss_bp` | `number` | Yes | Expected default-loss adjustment expressed in basis points. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_basis_trade_analyzer",
  "arguments": {
    "cash_spread_bp": 0,
    "cds_spread_bp": 0,
    "repo_rate_bp": 0,
    "funding_rate_bp": 0,
    "expected_loss_bp": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_basis_trade_analyzer"`.
