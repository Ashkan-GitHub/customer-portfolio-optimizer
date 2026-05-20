"""Synthetic data utilities for deterministic examples."""

from __future__ import annotations

import numpy as np

from .schemas import Asset, CustomerProfile, MarketData, OptimizationRequest


def create_synthetic_market_data() -> MarketData:
    """Create deterministic market data for example use and tests."""
    assets = [
        Asset(asset_id="us_eq", name="US Equity", asset_class="equity"),
        Asset(asset_id="intl_eq", name="International Equity", asset_class="equity"),
        Asset(asset_id="us_bond", name="US Bonds", asset_class="fixed_income"),
        Asset(asset_id="gl_bond", name="Global Bonds", asset_class="fixed_income"),
        Asset(asset_id="real", name="Real Assets", asset_class="alternatives"),
    ]
    expected_returns = [0.085, 0.078, 0.038, 0.033, 0.06]
    vol = np.array([0.18, 0.20, 0.07, 0.08, 0.12])
    corr = np.array([
        [1.00, 0.82, 0.18, 0.12, 0.45],
        [0.82, 1.00, 0.15, 0.10, 0.40],
        [0.18, 0.15, 1.00, 0.75, 0.20],
        [0.12, 0.10, 0.75, 1.00, 0.18],
        [0.45, 0.40, 0.20, 0.18, 1.00],
    ])
    cov = np.outer(vol, vol) * corr
    return MarketData(
        assets=assets,
        expected_returns=expected_returns,
        covariance_matrix=cov.round(8).tolist(),
        correlation_matrix=corr.round(8).tolist(),
    )


def create_example_customer() -> CustomerProfile:
    """Create a representative customer profile."""
    return CustomerProfile(
        customer_id="CUST-1001",
        age=38,
        annual_income=145000,
        investable_assets=320000,
        investment_horizon_years=18,
        risk_tolerance=7,
        liquidity_needs="medium",
        objectives=["growth", "retirement"],
    )


def create_example_request() -> OptimizationRequest:
    """Create a complete optimization request."""
    return OptimizationRequest(
        customer=create_example_customer(),
        market_data=create_synthetic_market_data(),
        max_asset_weight=0.5,
    )
