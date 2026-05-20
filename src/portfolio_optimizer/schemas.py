"""Pydantic schemas for the portfolio optimization domain."""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class CustomerProfile(BaseModel):
    customer_id: str
    age: int = Field(..., ge=18, le=100)
    annual_income: float = Field(..., ge=0)
    investable_assets: float = Field(..., ge=0)
    investment_horizon_years: int = Field(..., ge=1, le=60)
    risk_tolerance: int = Field(..., ge=1, le=10)
    liquidity_needs: str = Field(default="medium")
    objectives: List[str] = Field(default_factory=list)

    @field_validator("risk_tolerance")
    @classmethod
    def validate_risk_tolerance(cls, value: int) -> int:
        if not 1 <= value <= 10:
            raise ValueError("risk_tolerance must be between 1 and 10")
        return value


class Asset(BaseModel):
    asset_id: str
    name: str
    asset_class: str


class MarketData(BaseModel):
    assets: List[Asset]
    expected_returns: List[float]
    covariance_matrix: List[List[float]]
    correlation_matrix: Optional[List[List[float]]] = None

    @model_validator(mode="after")
    def validate_shapes(self) -> "MarketData":
        n = len(self.assets)
        if len(self.expected_returns) != n:
            raise ValueError("expected_returns length must match assets length")
        if len(self.covariance_matrix) != n or any(len(row) != n for row in self.covariance_matrix):
            raise ValueError("covariance_matrix must be square with size equal to assets length")
        if self.correlation_matrix is not None:
            if len(self.correlation_matrix) != n or any(len(row) != n for row in self.correlation_matrix):
                raise ValueError("correlation_matrix must be square with size equal to assets length")
        return self


class OptimizationRequest(BaseModel):
    customer: CustomerProfile
    market_data: MarketData
    max_asset_weight: Optional[float] = Field(default=None, gt=0, le=1)

    @field_validator("max_asset_weight")
    @classmethod
    def validate_max_asset_weight(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and not (0 < value <= 1):
            raise ValueError("max_asset_weight must be in (0, 1]")
        return value


class PortfolioResult(BaseModel):
    weights: Dict[str, float]
    expected_return: float
    volatility: float
    utility: float
    method: str
    explanation: str
