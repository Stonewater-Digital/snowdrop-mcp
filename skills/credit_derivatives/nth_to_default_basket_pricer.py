"""
Executive Summary: Prices nth-to-default baskets via Gaussian copula Monte Carlo with systematic risk.
Inputs: default_probabilities (list[float]), pairwise_correlation (float), recovery_rate (float), notional (float), nth (int), horizon_years (float), discount_rate (float), num_paths (int)
Outputs: status (str), timestamp (str), data (dict)
MCP Tool Name: nth_to_default_basket_pricer
"""
import logging
import math
import random
from datetime import datetime, timezone
from statistics import NormalDist
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")
ND = NormalDist()

TOOL_META = {
    "name": "nth_to_default_basket_pricer",
    "description": (
        "Monte Carlo Gaussian copula model (Li, 2000) for nth-to-default baskets with "
        "systematic correlation and discounted loss metrics."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "default_probabilities": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Marginal default probabilities over the horizon for each reference obligor."
            },
            "pairwise_correlation": {
                "type": "number",
                "description": "Asset correlation applied uniformly across the basket."
            },
            "recovery_rate": {
                "type": "number",
                "description": "Expected recovery rate applied to each obligor (0-1)."
            },
            "notional": {
                "type": "number",
                "description": "Tranche notional in currency units."
            },
            "nth": {
                "type": "integer",
                "description": "Order of default that triggers the tranche."
            },
            "horizon_years": {
                "type": "number",
                "description": "Tenor of the basket in years."
            },
            "discount_rate": {
                "type": "number",
                "description": "Continuous risk-free discount rate for PV calculations."
            },
            "num_paths": {
                "type": "integer",
                "description": "Monte Carlo path count (>=2000 recommended)."
            }
        },
        "required": [
            "default_probabilities",
            "pairwise_correlation",
            "recovery_rate",
            "notional",
            "nth",
            "horizon_years",
            "discount_rate",
            "num_paths"
        ]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["status", "timestamp"]
    }
}


def nth_to_default_basket_pricer(**kwargs: Any) -> dict[str, Any]:
    try:
        probs = _validate_probability_vector(kwargs["default_probabilities"])
        rho = float(kwargs["pairwise_correlation"])
        recovery = float(kwargs["recovery_rate"])
        notional = float(kwargs["notional"])
        nth = int(kwargs["nth"])
        horizon = float(kwargs["horizon_years"])
        discount_rate = float(kwargs["discount_rate"])
        num_paths = max(1000, int(kwargs["num_paths"]))

        if not (0.0 <= recovery < 1.0):
            raise ValueError("recovery_rate must be between 0 and 1")
        if not (0.0 <= rho < 1.0):
            raise ValueError("pairwise_correlation must be in [0,1)")
        if nth < 1 or nth > len(probs):
            raise ValueError("nth order must be within basket size")

        systemic_weight = math.sqrt(rho)
        idio_weight = math.sqrt(1 - rho)
        z_thresholds = [ND.inv_cdf(p) for p in probs]
        rand = random.Random(42)

        hits = 0
        path_losses = []
        for _ in range(num_paths):
            systemic = rand.gauss(0.0, 1.0)
            defaults = 0
            loss = 0.0
            for z_thr in z_thresholds:
                latent = systemic_weight * systemic + idio_weight * rand.gauss(0.0, 1.0)
                if latent <= z_thr:
                    defaults += 1
                    loss += (1 - recovery)
                if defaults >= nth:
                    break
            if defaults >= nth:
                hits += 1
                path_losses.append((1 - recovery) * notional)
            else:
                path_losses.append(loss / len(probs) * notional)

        trigger_probability = hits / num_paths
        discount_factor = math.exp(-discount_rate * horizon)
        expected_loss = discount_factor * (sum(path_losses) / num_paths)
        tranche_pv = trigger_probability * (1 - recovery) * notional * discount_factor

        data = {
            "trigger_probability": trigger_probability,
            "discount_factor": discount_factor,
            "expected_loss": expected_loss,
            "tranche_pv": tranche_pv,
            "loss_given_trigger": (1 - recovery) * notional,
            "simulated_paths": num_paths
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error("nth_to_default_basket_pricer failed: %s", e)
        _log_lesson(f"nth_to_default_basket_pricer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _validate_probability_vector(probs: Sequence[Any]) -> list[float]:
    if not probs:
        raise ValueError("default_probabilities must be non-empty")
    cleaned = []
    for value in probs:
        p = float(value)
        if not 0.0 <= p < 1.0:
            raise ValueError("probabilities must be in [0,1)")
        cleaned.append(p)
    return cleaned


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
