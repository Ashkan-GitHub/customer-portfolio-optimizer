"""Risk policy mapping from customer profile to optimizer targets."""

from __future__ import annotations

from typing import Dict, Tuple

from .schemas import CustomerProfile


def _allocation_bounds(risk_tolerance: int) -> Tuple[float, float]:
    if risk_tolerance <= 3:
        return 0.0, 0.45
    if risk_tolerance <= 6:
        return 0.0, 0.60
    return 0.0, 0.75


def map_customer_to_risk_policy(customer: CustomerProfile) -> Dict[str, float]:
    """Map customer inputs to optimization policy parameters."""
    rt = customer.risk_tolerance
    horizon_bonus = min(customer.investment_horizon_years / 40.0, 0.5)
    liquidity_penalty = {
        "high": 0.15,
        "medium": 0.05,
        "low": 0.0,
    }.get(customer.liquidity_needs.lower(), 0.05)

    risk_aversion = max(1.0, 8.0 - 0.6 * rt - 2.0 * horizon_bonus + liquidity_penalty)
    max_volatility = min(0.08 + 0.012 * rt + 0.02 * horizon_bonus - 0.01 * liquidity_penalty, 0.22)
    min_return = max(0.02, 0.02 + 0.004 * rt + 0.003 * horizon_bonus - 0.002 * liquidity_penalty)
    lower_bound, upper_bound = _allocation_bounds(rt)

    return {
        "risk_aversion": round(risk_aversion, 6),
        "max_volatility": round(max_volatility, 6),
        "min_return": round(min_return, 6),
        "min_weight": round(lower_bound, 6),
        "max_weight": round(upper_bound, 6),
    }
