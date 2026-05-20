from __future__ import annotations

import math

import pytest

from portfolio_optimizer.data import create_example_request, create_synthetic_market_data
from portfolio_optimizer.optimizer import optimize_portfolio
from portfolio_optimizer.risk_mapping import map_customer_to_risk_policy
from portfolio_optimizer.schemas import CustomerProfile, MarketData


def test_weights_sum_to_one() -> None:
    request = create_example_request()
    result = optimize_portfolio(request)
    assert math.isclose(sum(result.weights.values()), 1.0, rel_tol=1e-6, abs_tol=1e-6)


def test_weights_respect_max_weight() -> None:
    request = create_example_request()
    request.max_asset_weight = 0.4
    result = optimize_portfolio(request)
    assert all(weight <= 0.400001 for weight in result.weights.values())


def test_correlation_validation_shape() -> None:
    market = create_synthetic_market_data()
    with pytest.raises(ValueError):
        MarketData(
            assets=market.assets,
            expected_returns=market.expected_returns,
            covariance_matrix=market.covariance_matrix,
            correlation_matrix=[[1.0, 0.1], [0.1, 1.0]],
        )


def test_risk_mapping_increases_capacity_with_higher_tolerance() -> None:
    conservative = CustomerProfile(
        customer_id="A",
        age=45,
        annual_income=100000,
        investable_assets=200000,
        investment_horizon_years=10,
        risk_tolerance=2,
        liquidity_needs="medium",
        objectives=["preservation"],
    )
    aggressive = CustomerProfile(
        customer_id="B",
        age=45,
        annual_income=100000,
        investable_assets=200000,
        investment_horizon_years=10,
        risk_tolerance=9,
        liquidity_needs="medium",
        objectives=["growth"],
    )
    policy_low = map_customer_to_risk_policy(conservative)
    policy_high = map_customer_to_risk_policy(aggressive)

    assert policy_high["risk_aversion"] < policy_low["risk_aversion"]
    assert policy_high["max_volatility"] > policy_low["max_volatility"]
    assert policy_high["min_return"] > policy_low["min_return"]
