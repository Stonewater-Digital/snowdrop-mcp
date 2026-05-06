---
skill: france_amf_whitepaper_audit
category: compliance
description: Audits a token offering whitepaper against French AMF requirements under the Pacte Law (Loi n° 2019-486) and AMF General Regulation (RG AMF) Articles 712-1 to 712-23. Scores completeness, flags missing mandatory sections, and determines ICO visa eligibility.
tier: premium
inputs: none
---

# France Amf Whitepaper Audit

## Description
Audits a token offering whitepaper against French AMF requirements under the Pacte Law (Loi n° 2019-486) and AMF General Regulation (RG AMF) Articles 712-1 to 712-23. Scores completeness, flags missing mandatory sections, and determines ICO visa eligibility. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "france_amf_whitepaper_audit",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "france_amf_whitepaper_audit"`.
