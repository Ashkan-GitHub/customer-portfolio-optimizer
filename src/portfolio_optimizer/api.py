"""FastAPI application exposing the optimizer."""

from __future__ import annotations

from fastapi import FastAPI

from .optimizer import optimize_portfolio
from .schemas import OptimizationRequest, PortfolioResult

app = FastAPI(title="Customer Portfolio Optimizer", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/optimize", response_model=PortfolioResult)
def optimize(request: OptimizationRequest) -> PortfolioResult:
    return optimize_portfolio(request)
