---
skill: esg_screened_optimizer
category: portfolio_construction
description: Delivers a constrained mean-variance allocation subject to minimum ESG score, sector exclusions, and sector caps consistent with EU SFDR Article 8 screening.
tier: free
inputs: expected_returns, covariance_matrix, esg_scores, sector_labels
---

# Esg Screened Optimizer

## Description
Delivers a constrained mean-variance allocation subject to minimum ESG score, sector exclusions, and sector caps consistent with EU SFDR Article 8 screening.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `expected_returns` | `array` | Yes | Vector of expected returns per asset (decimal). |
| `covariance_matrix` | `array` | Yes | Covariance matrix for the same asset order. |
| `esg_scores` | `array` | Yes | Numeric ESG scores (0-100) for each asset. |
| `sector_labels` | `array` | Yes | GICS/NAICS sector tag for each asset. |
| `min_esg_score` | `number` | No | Minimum ESG score required (default 60). |
| `excluded_sectors` | `array` | No | List of sector labels that are fully excluded. |
| `max_sector_weight` | `number` | No | Maximum percentage weight per sector (default 0.25). |
| `risk_aversion` | `number` | No | Risk aversion parameter for mean-variance solution (default 3). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "esg_screened_optimizer",
  "arguments": {
    "expected_returns": [],
    "covariance_matrix": [],
    "esg_scores": [],
    "sector_labels": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "esg_screened_optimizer"`.
