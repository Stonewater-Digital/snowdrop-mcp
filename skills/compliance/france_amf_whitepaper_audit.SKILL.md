---
skill: france_amf_whitepaper_audit
category: compliance
description: Audits a token offering whitepaper against French AMF requirements under the Pacte Law (Loi n° 2019-486) and AMF General Regulation (RG AMF) Articles 712-1 to 712-23. Scores completeness, flags missing mandatory sections, and determines ICO visa eligibility.
tier: premium
inputs: whitepaper_data
---

# France Amf Whitepaper Audit

## Description
Audits a token offering whitepaper against French AMF requirements under the Pacte Law (Loi n° 2019-486) and AMF General Regulation (RG AMF) Articles 712-1 to 712-23. Scores completeness, flags missing mandatory sections, and determines ICO visa eligibility. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `whitepaper_data` | `object` | Yes | Token offering whitepaper content including sections, issuer details, token economics, risk factors, and use of proceeds for AMF audit |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "france_amf_whitepaper_audit",
  "arguments": {
    "whitepaper_data": {
      "issuer_name": "TechToken SAS",
      "token_type": "utility",
      "sections": ["project_description", "risk_factors", "use_of_proceeds"],
      "target_raise_eur": 5000000
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "france_amf_whitepaper_audit"`.
