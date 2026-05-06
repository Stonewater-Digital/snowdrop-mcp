---
skill: ireland_ica_reporting
category: compliance
description: Generates Irish Central Bank (CBI) reporting data for Irish Collective Asset-management Vehicles (ICAVs) under the Irish Collective Asset-management Vehicles Act 2015 and CBI UCITS/AIF Rulebooks. Supports both UCITS and AIFMD structures with sub-fund disaggregation and CBI deadline computation.
tier: premium
inputs: none
---

# Ireland Ica Reporting

## Description
Generates Irish Central Bank (CBI) reporting data for Irish Collective Asset-management Vehicles (ICAVs) under the Irish Collective Asset-management Vehicles Act 2015 and CBI UCITS/AIF Rulebooks. Supports both UCITS and AIFMD structures with sub-fund disaggregation and CBI deadline computation. (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ireland_ica_reporting",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ireland_ica_reporting"`.
