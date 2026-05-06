---
skill: loan_cds_basis_analyzer
category: credit_derivatives
description: Decomposes LCDS-cash loan basis into funding, liquidity, and recovery adjustments for basis trades.
tier: free
inputs: loan_spread_bp, lcds_spread_bp, funding_basis_bp, recovery_rate, maturity_years
---

# Loan Cds Basis Analyzer

## Description
Decomposes LCDS-cash loan basis into funding, liquidity, and recovery adjustments for basis trades.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `loan_spread_bp` | `number` | Yes | Observed leveraged loan spread (L+bp). |
| `lcds_spread_bp` | `number` | Yes | Quoted LCDS spread for the same borrower in basis points. |
| `funding_basis_bp` | `number` | Yes | Liquidity or funding discount to LIBOR/EURIBOR in basis points. |
| `recovery_rate` | `number` | Yes | Assumed recovery for secured loans (0-1). |
| `maturity_years` | `number` | Yes | Remaining maturity used for PV01 conversion. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "loan_cds_basis_analyzer",
  "arguments": {
    "loan_spread_bp": 0,
    "lcds_spread_bp": 0,
    "funding_basis_bp": 0,
    "recovery_rate": 0,
    "maturity_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "loan_cds_basis_analyzer"`.
