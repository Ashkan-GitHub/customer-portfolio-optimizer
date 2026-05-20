"""Explanation utilities for optimization outputs."""

from __future__ import annotations

from typing import Dict

from .schemas import CustomerProfile, PortfolioResult


def explain_portfolio_result(
    customer: CustomerProfile,
    result: PortfolioResult,
    policy: Dict[str, float],
) -> str:
    """Create a concise, human-readable explanation of the portfolio result."""
    top_allocations = sorted(result.weights.items(), key=lambda item: item[1], reverse=True)[:3]
    top_text = ", ".join(f"{name} ({weight:.1%})" for name, weight in top_allocations)
    return (
        f"Customer {customer.customer_id} with risk tolerance {customer.risk_tolerance}/10 "
        f"and a {customer.investment_horizon_years}-year horizon was mapped to risk aversion "
        f"{policy['risk_aversion']:.2f}, minimum return {policy['min_return']:.2%}, and "
        f"maximum volatility {policy['max_volatility']:.2%}. "
        f"The optimizer selected a diversified allocation led by {top_text}. "
        f"The resulting portfolio has expected return {result.expected_return:.2%} and "
        f"volatility {result.volatility:.2%} using method '{result.method}'."
    )
