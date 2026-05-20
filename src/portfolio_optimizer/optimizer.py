"""Optimization engine for customer-aware portfolios."""

from __future__ import annotations

from typing import Dict, Tuple

import numpy as np
from scipy.optimize import minimize

from .risk_mapping import map_customer_to_risk_policy
from .schemas import OptimizationRequest, PortfolioResult


def _portfolio_return(weights: np.ndarray, mu: np.ndarray) -> float:
    return float(mu @ weights)


def _portfolio_variance(weights: np.ndarray, cov: np.ndarray) -> float:
    return float(weights @ cov @ weights)


def _portfolio_volatility(weights: np.ndarray, cov: np.ndarray) -> float:
    return float(np.sqrt(max(_portfolio_variance(weights, cov), 0.0)))


def _solve(
    mu: np.ndarray,
    cov: np.ndarray,
    risk_aversion: float,
    min_return: float | None,
    max_volatility: float | None,
    max_weight: float | None,
    objective_name: str,
) -> Tuple[np.ndarray, bool, str]:
    n = len(mu)
    initial = np.full(n, 1.0 / n)
    upper = max_weight if max_weight is not None else 1.0
    bounds = [(0.0, upper) for _ in range(n)]

    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0}]
    if min_return is not None:
        constraints.append({"type": "ineq", "fun": lambda w, mr=min_return: _portfolio_return(w, mu) - mr})
    if max_volatility is not None:
        constraints.append({"type": "ineq", "fun": lambda w, mv=max_volatility: mv - _portfolio_volatility(w, cov)})

    if objective_name == "utility":
        def objective(w: np.ndarray) -> float:
            return -(_portfolio_return(w, mu) - risk_aversion * _portfolio_variance(w, cov))
    else:
        def objective(w: np.ndarray) -> float:
            return _portfolio_variance(w, cov)

    result = minimize(
        objective,
        initial,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 200, "ftol": 1e-9, "disp": False},
    )
    weights = np.array(result.x if result.success else initial, dtype=float)
    weights = np.clip(weights, 0.0, upper)
    total = weights.sum()
    if total > 0:
        weights = weights / total
    return weights, bool(result.success), str(result.message)


def optimize_portfolio(request: OptimizationRequest) -> PortfolioResult:
    """Optimize a portfolio using customer-aware risk policy and market data."""
    policy = map_customer_to_risk_policy(request.customer)
    mu = np.array(request.market_data.expected_returns, dtype=float)
    cov = np.array(request.market_data.covariance_matrix, dtype=float)
    names = [asset.name for asset in request.market_data.assets]

    effective_max_weight = request.max_asset_weight
    if effective_max_weight is None:
        effective_max_weight = policy["max_weight"]
    else:
        effective_max_weight = min(effective_max_weight, policy["max_weight"])

    weights, success, message = _solve(
        mu=mu,
        cov=cov,
        risk_aversion=policy["risk_aversion"],
        min_return=policy["min_return"],
        max_volatility=policy["max_volatility"],
        max_weight=effective_max_weight,
        objective_name="utility",
    )
    method = "mean_variance_utility"

    if not success:
        weights, _, fallback_message = _solve(
            mu=mu,
            cov=cov,
            risk_aversion=policy["risk_aversion"],
            min_return=None,
            max_volatility=policy["max_volatility"],
            max_weight=effective_max_weight,
            objective_name="min_variance",
        )
        method = f"min_variance_fallback: {fallback_message or message}"

    expected_return = _portfolio_return(weights, mu)
    volatility = _portfolio_volatility(weights, cov)
    utility = expected_return - policy["risk_aversion"] * _portfolio_variance(weights, cov)

    from .explain import explain_portfolio_result

    result = PortfolioResult(
        weights={name: round(float(weight), 6) for name, weight in zip(names, weights)},
        expected_return=round(expected_return, 6),
        volatility=round(volatility, 6),
        utility=round(utility, 6),
        method=method,
        explanation="",
    )
    result.explanation = explain_portfolio_result(request.customer, result, policy)
    return result
