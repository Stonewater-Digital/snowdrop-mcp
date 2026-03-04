"""Calculate beta of a commodity basket against broad index."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Sequence

TOOL_META: dict[str, Any] = {
    "name": "commodity_beta_calculator",
    "description": (
        "Estimates OLS beta, alpha, correlation, and annualized tracking error of a commodity "
        "return series against a benchmark. Returns are in decimal form (e.g. 0.02 = 2%)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "commodity_returns": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Periodic return series for the commodity (decimal, e.g. 0.01 = 1%).",
                "minItems": 2,
            },
            "benchmark_returns": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Periodic return series for the benchmark (same length and frequency).",
                "minItems": 2,
            },
            "periods_per_year": {
                "type": "number",
                "default": 252,
                "description": "Number of return periods per year for annualization (252=daily, 12=monthly).",
            },
        },
        "required": ["commodity_returns", "benchmark_returns"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "beta": {"type": "number"},
            "alpha_per_period": {"type": "number"},
            "correlation": {"type": "number"},
            "annualized_tracking_error_pct": {"type": "number"},
            "r_squared": {"type": "number"},
            "n_observations": {"type": "integer"},
            "timestamp": {"type": "string"},
        },
    },
}


def commodity_beta_calculator(
    commodity_returns: Sequence[float],
    benchmark_returns: Sequence[float],
    periods_per_year: float = 252,
    **_: Any,
) -> dict[str, Any]:
    """Return OLS beta, alpha, correlation, and annualized tracking error.

    Args:
        commodity_returns: Asset return series (decimal form, same length as benchmark).
        benchmark_returns: Benchmark return series (decimal form).
        periods_per_year: Periods per year for annualizing tracking error (default 252).

    Returns:
        dict with status, beta, alpha_per_period, correlation, annualized_tracking_error_pct,
        r_squared, and n_observations.

    OLS regression: r_commodity = alpha + beta * r_benchmark + epsilon

    Beta:
        β = Cov(r_c, r_b) / Var(r_b)
        Using sample covariance (n-1 denominator).

    Tracking error (annualized):
        TE = std_dev(residuals) * sqrt(periods_per_year)
        where residuals = r_c - (alpha + beta * r_b)

    Correlation:
        ρ = Cov(r_c, r_b) / (σ_c * σ_b)

    R² = ρ²
    """
    try:
        n = len(commodity_returns)
        if n != len(benchmark_returns):
            raise ValueError("commodity_returns and benchmark_returns must be the same length")
        if n < 3:
            raise ValueError("Need at least 3 observations for OLS")
        if periods_per_year <= 0:
            raise ValueError("periods_per_year must be positive")

        com = [float(v) for v in commodity_returns]
        bench = [float(v) for v in benchmark_returns]

        mean_c = sum(com) / n
        mean_b = sum(bench) / n

        # Sample covariance and variance (n-1 denominator)
        cov = sum((com[i] - mean_c) * (bench[i] - mean_b) for i in range(n)) / (n - 1)
        var_b = sum((v - mean_b) ** 2 for v in bench) / (n - 1)
        var_c = sum((v - mean_c) ** 2 for v in com) / (n - 1)

        if var_b <= 0:
            raise ValueError("Benchmark return series has zero variance")

        beta = cov / var_b
        alpha = mean_c - beta * mean_b

        # Residuals from OLS fit
        residuals = [com[i] - (alpha + beta * bench[i]) for i in range(n)]
        # Sample variance of residuals
        mean_res = sum(residuals) / n
        var_res = sum((r - mean_res) ** 2 for r in residuals) / (n - 1) if n > 1 else 0.0
        te_per_period = math.sqrt(max(var_res, 0.0))
        te_annual = te_per_period * math.sqrt(periods_per_year)

        # Correlation and R²
        denom = math.sqrt(var_b * var_c) if var_b > 0 and var_c > 0 else 0.0
        correlation = cov / denom if denom > 0 else 0.0
        r_squared = correlation ** 2

        return {
            "status": "success",
            "beta": round(beta, 4),
            "alpha_per_period": round(alpha, 6),
            "correlation": round(correlation, 4),
            "annualized_tracking_error_pct": round(te_annual * 100.0, 4),
            "r_squared": round(r_squared, 4),
            "n_observations": n,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("commodity_beta_calculator", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
