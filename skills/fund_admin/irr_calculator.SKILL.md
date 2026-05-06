---
skill: irr_calculator
category: fund_admin
description: Computes IRR via Newton-Raphson iteration for periodic cash flows. Requires at least one sign change in the cash flow series.
tier: premium
inputs: cash_flows, guess_rate_pct, max_iterations, tolerance
---

# Irr Calculator

## Description
Computes IRR via Newton-Raphson iteration for periodic cash flows. Requires at least one sign change in the cash flow series. Returns IRR as an annualized percentage. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| cash_flows | array | Yes | Ordered sequence of periodic cash flows (negative = capital outflows/calls, positive = distributions/proceeds) |
| guess_rate_pct | number | No | Initial IRR guess percentage for Newton-Raphson convergence (default: 10.0) |
| max_iterations | number | No | Maximum number of Newton-Raphson iterations before reporting non-convergence (default: 1000) |
| tolerance | number | No | Convergence tolerance for the NPV residual; smaller values yield greater precision (default: 1e-8) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "irr_calculator",
  "arguments": {
    "cash_flows": [-10000000, -5000000, 0, 2000000, 8000000, 18000000],
    "guess_rate_pct": 10.0,
    "max_iterations": 1000,
    "tolerance": 1e-8
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "irr_calculator"`.
