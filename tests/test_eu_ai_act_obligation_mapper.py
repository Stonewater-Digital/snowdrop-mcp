"""Unit tests for the EU AI Act obligation mapper skill."""
from __future__ import annotations

import unittest

from skills.compliance.eu_ai_act_obligation_mapper import eu_ai_act_obligation_mapper


class TestEUAiActObligationMapper(unittest.TestCase):
    """Validate mapping and validation logic."""

    def test_provider_high_risk_obligations(self) -> None:
        result = eu_ai_act_obligation_mapper(
            role="provider",
            system_type="high_risk_annex_iii",
            use_case="credit scoring for consumer lending",
            deployment_stage="pre_market",
            detail_level="full",
        )
        self.assertEqual(result["status"], "success")
        obligations = result["data"]["matched_obligations"]
        ids = [item["id"] for item in obligations]
        self.assertIn("HRA-PROVIDER-RMS", ids)
        # Detail level should convey full metadata.
        first = obligations[0]
        self.assertEqual(first["detail_level"], "full")
        self.assertIn("match_score", first)
        self.assertTrue(any("keyword" in reason for reason in first["match_reasons"]))

    def test_limited_risk_transparency(self) -> None:
        result = eu_ai_act_obligation_mapper(
            role="deployer",
            system_type="limited_risk",
            use_case="customer service chatbot",
        )
        self.assertEqual(result["status"], "success")
        ids = [item["id"] for item in result["data"]["matched_obligations"]]
        self.assertIn("LIMITED-RISK-TRANSPARENCY", ids)

    def test_invalid_role_returns_error(self) -> None:
        result = eu_ai_act_obligation_mapper(
            role="astronaut",
            system_type="high_risk_annex_iii",
        )
        self.assertEqual(result["status"], "error")
        self.assertIn("Unsupported role", result["data"]["error"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
