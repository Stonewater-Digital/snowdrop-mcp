"""
Executive Summary: Prices first-loss (equity) tranches using a large homogeneous portfolio copula with base-correlation inputs.
Inputs: portfolio_notional (float), default_probability (float), recovery_rate (float), attachment_point (float), detachment_point (float), base_correlation_attachment (float), base_correlation_detachment (float), num_paths (int), discount_rate (float), horizon_years (float)
Outputs: status (str), timestamp (str), data (dict)
MCP Tool Name: first_loss_tranche_pricer
"""
import logging
import math
import random
from datetime import datetime, timezone
from statistics import NormalDist
from typing import Any

logger = logging.getLogger("snowdrop.skills")
ND = NormalDist()

TOOL_META = {
    "name": "first_loss_tranche_pricer",
    "description": (
        "Monte Carlo Vasicek/Li large pool approximation for equity tranches using base-correlation "
        "averaging to determine the effective copula correlation."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio_notional": {"type": "number", "description": "Total underlying notional."},
            "default_probability": {"type": "number", "description": "Portfolio default probability over horizon (decimal)."},
            "recovery_rate": {"type": "number", "description": "Recovery assumption (decimal)."},
            "attachment_point": {"type": "number", "description": "Equity tranche attachment in fractional terms."},
            "detachment_point": {"type": "number", "description": "Equity tranche detachment (fraction)."},
            "base_correlation_attachment": {"type": "number", "description": "Base correlation at the attachment point."},
            "base_correlation_detachment": {"type": "number", "description": "Base correlation at the detachment point."},
            "num_paths": {"type": "integer", "description": "Monte Carlo path count (>=3000 recommended)."},
            "discount_rate": {"type": "number", "description": "Risk-free rate for PV."},
            "horizon_years": {"type": "number", "description": "Maturity in years."}
        },
        "required": [
            "portfolio_notional",
            "default_probability",
            "recovery_rate",
            "attachment_point",
            "detachment_point",
            "base_correlation_attachment",
            "base_correlation_detachment",
            "num_paths",
            "discount_rate",
            "horizon_years"
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


def first_loss_tranche_pricer(**kwargs: Any) -> dict[str, Any]:
    try:
        notional = float(kwargs["portfolio_notional"])
        pd = float(kwargs["default_probability"])
        recovery = float(kwargs["recovery_rate"])
        attach = float(kwargs["attachment_point"])
        detach = float(kwargs["detachment_point"])
        rho_a = float(kwargs["base_correlation_attachment"])
        rho_b = float(kwargs["base_correlation_detachment"])
        num_paths = max(2000, int(kwargs["num_paths"]))
        discount_rate = float(kwargs["discount_rate"])
        horizon = float(kwargs["horizon_years"])

        if not 0 <= attach < detach <= 1:
            raise ValueError("attachment/detachment must satisfy 0<=A<D<=1")
        if not 0.0 <= recovery < 1.0:
            raise ValueError("recovery_rate must lie in [0,1)")
        if not 0.0 < pd < 1.0:
            raise ValueError("default_probability must be in (0,1)")

        effective_rho = 0.5 * (rho_a + rho_b)
        effective_rho = min(max(effective_rho, 0.0001), 0.999)
        tranche_notional = (detach - attach) * notional

        z_default = ND.inv_cdf(pd)
        rand = random.Random(1357)
        tranche_losses = []
        systemic_weight = math.sqrt(effective_rho)
        idio_weight = math.sqrt(1 - effective_rho)
        for _ in range(num_paths):
            systemic = rand.gauss(0.0, 1.0)
            cond_pd = ND.cdf((z_default - systemic_weight * systemic) / idio_weight)
            cond_pd = min(max(cond_pd, 0.0), 1.0)
            loss_fraction = (1 - recovery) * cond_pd
            tranche_loss = max(min(loss_fraction - attach, detach - attach), 0.0)
            tranche_losses.append(tranche_loss * notional)

        expected_loss = sum(tranche_losses) / num_paths
        discount_factor = math.exp(-discount_rate * horizon)
        pv_loss = expected_loss * discount_factor
        expected_return = tranche_notional - pv_loss

        data = {
            "expected_tranche_loss": expected_loss,
            "present_value_loss": pv_loss,
            "expected_return": expected_return,
            "effective_correlation": effective_rho,
            "discount_factor": discount_factor,
            "simulated_paths": num_paths
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error("first_loss_tranche_pricer failed: %s", e)
        _log_lesson(f"first_loss_tranche_pricer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
