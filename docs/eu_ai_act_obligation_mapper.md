# EU AI Act Obligation Mapper

Snowdrop now ships a compliance skill that turns role + risk-class context into a
curated list of EU AI Act obligations. The mapper combines the reference data in
`state/eu_ai_act_obligations.json` with simple heuristics (risk overlap,
deployment stage, keyword hits) so agents can quickly see what needs to be in
place before placing a system on the EU market.

## Inputs

| Field | Type | Notes |
| --- | --- | --- |
| `role` | `string` | Economic actor (provider, deployer, importer, distributor, authorized_representative, product_manufacturer, general_purpose_provider, general_purpose_integrator). |
| `system_type` | `string` | Primary risk class. Use `high_risk_annex_iii`, `high_risk_annex_i`, `limited_risk`, `general_purpose`, `general_purpose_integrated`, or `minimal_risk`. |
| `system_types` | `array[string]` | Optional list if multiple classes apply. |
| `deployment_stage` | `string` | One of `pre_market`, `post_market`, `monitoring`, `incident`. Filters obligations to that phase. |
| `use_case` | `string` | Free text for keyword matching (e.g., "credit scoring"). |
| `detail_level` | `string` | `summary` (default) or `full`. Full adds deliverables/evidence lists. |

## Output

The skill returns:

- `matched_obligations`: ordered by match score with match reasons.
- `coverage_note`: message when no obligations triggered.
- `reference_version`: helps track when the JSON map was last updated.

Example snippet:

```json
{
  "status": "success",
  "data": {
    "role": "provider",
    "system_types": ["high_risk_annex_iii"],
    "matched_obligations": [
      {
        "id": "HRA-PROVIDER-RMS",
        "title": "Risk management system",
        "summary": "Establish, document, implement...",
        "articles": ["Article 9", "Annex VII"],
        "match_reasons": [
          "risk_class match: high_risk_annex_iii",
          "keyword match: credit scoring"
        ],
        "match_score": 3.1
      }
    ]
  }
}
```

## Reference data

- File: `state/eu_ai_act_obligations.json`
- Contains metadata, role aliases, risk classes, and 12 core obligations covering
  providers, deployers, importers/distributors, and GPAI actors. The file is
  intentionally human-readable and versioned so compliance reviewers can update
  obligations without editing Python code.

## Tests

```
python -m unittest tests.test_eu_ai_act_obligation_mapper
```

These tests cover:

- Provider/high-risk happy path with keyword boost.
- Limited-risk transparency obligations for deployers.
- Error handling for unsupported roles.
