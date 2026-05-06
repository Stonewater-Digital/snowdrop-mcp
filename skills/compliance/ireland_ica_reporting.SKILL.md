---
skill: ireland_ica_reporting
category: compliance
description: Generates Irish Central Bank (CBI) reporting data for Irish Collective Asset-management Vehicles (ICAVs) under the Irish Collective Asset-management Vehicles Act 2015 and CBI UCITS/AIF Rulebooks. Supports both UCITS and AIFMD structures with sub-fund disaggregation and CBI deadline computation.
tier: premium
inputs: fund_data
---

# Ireland Ica Reporting

## Description
Generates Irish Central Bank (CBI) reporting data for Irish Collective Asset-management Vehicles (ICAVs) under the Irish Collective Asset-management Vehicles Act 2015 and CBI UCITS/AIF Rulebooks. Supports both UCITS and AIFMD structures with sub-fund disaggregation and CBI deadline computation. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fund_data` | `object` | Yes | ICAV fund details including structure type (UCITS/AIFMD), sub-fund list, NAV, reporting period, and CBI entity codes |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ireland_ica_reporting",
  "arguments": {
    "fund_data": {
      "fund_name": "Atlantic ICAV",
      "structure": "UCITS",
      "sub_funds": ["Atlantic Equity Sub-Fund", "Atlantic Bond Sub-Fund"],
      "reporting_period_end": "2026-03-31"
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ireland_ica_reporting"`.
