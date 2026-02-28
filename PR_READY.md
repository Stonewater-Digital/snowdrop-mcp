# PR Ready – EU AI Act obligation mapper

## Summary
- add `eu_ai_act_obligation_mapper` compliance skill that maps role + risk class
  inputs to curated EU AI Act obligations with scoring/explanations
- introduce structured reference data at `state/eu_ai_act_obligations.json`
  covering providers, deployers, importers, distributors, and GPAI actors
- document usage in `docs/eu_ai_act_obligation_mapper.md` and highlight the skill
  in the README
- add unit tests (`tests/test_eu_ai_act_obligation_mapper.py`) for the happy
  paths + validation errors

## Testing
```
python -m unittest tests.test_eu_ai_act_obligation_mapper
```

## Checklist
- [x] reference JSON committed
- [x] skill metadata + error logging
- [x] docs updated
- [x] tests passing locally

## TON Wallet
`UQDJVdxFU3HU1nfMyN965kWECxjcNUDiHp1YAoU78qGwG8XR`
