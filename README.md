# Customer Portfolio Optimizer

A customer-aware portfolio optimization engine built for practical analytics, backend API delivery, and testing.

## Project Overview

This project builds a deterministic portfolio optimization service that converts customer attributes, preferences, and market inputs into a suggested asset allocation.

The implementation focuses on:
- structured domain schemas with validation
- synthetic but reproducible market data generation
- customer-to-risk policy translation
- mean-variance portfolio optimization with practical constraints
- FastAPI service exposure
- CLI and Streamlit examples
- unit tests for core behaviors

## Problem Statement

Financial recommendation systems often fail when they optimize only against market data and ignore customer context. A realistic workflow should connect:
- who the customer is
- how much risk they can tolerate
- what constraints the business must respect
- what portfolio best fits those requirements

The problem solved here is: given a customer profile and market assumptions, how can we compute a valid, explainable, and deterministic portfolio recommendation?

## Solution

The solution combines:
1. **Validated request schemas** with Pydantic
2. **Risk mapping logic** that translates customer preferences into optimization targets
3. **SciPy SLSQP optimization** for constrained allocation selection
4. **Fallback behavior** to minimum-variance optimization if the primary objective fails
5. **Human-readable explanation generation**
6. **FastAPI deployment interface**
7. **CLI and Streamlit front ends**

The core objective maximizes risk-adjusted expected return:

`maximize mu^T w - lambda * w^T Sigma w`

subject to:
- weights sum to 1
- long-only allocation
- optional maximum asset weight
- optional minimum expected return
- optional maximum volatility

## Architecture / Code Structure

```text
customer-portfolio-optimizer/
├── README.md
├── pyproject.toml
├── .gitignore
├── Dockerfile
├── Makefile
├── examples/
│   └── example_request.json
├── app/
│   └── streamlit_app.py
├── src/
│   └── portfolio_optimizer/
│       ├── __init__.py
│       ├── api.py
│       ├── cli.py
│       ├── data.py
│       ├── explain.py
│       ├── optimizer.py
│       ├── risk_mapping.py
│       └── schemas.py
└── tests/
    └── test_optimizer.py
```

### Module Roles

- `schemas.py`: data contracts and validators
- `data.py`: deterministic synthetic market and customer examples
- `risk_mapping.py`: transforms customer inputs to optimization policy
- `optimizer.py`: portfolio optimization engine
- `explain.py`: recommendation narrative
- `api.py`: FastAPI service
- `cli.py`: command line entry point
- `streamlit_app.py`: lightweight UI
- `tests/test_optimizer.py`: behavior validation

## Optimization Formulation

Let:
- `w` = asset weights
- `mu` = expected returns vector
- `Sigma` = covariance matrix
- `lambda` = risk aversion parameter

Objective:
- maximize `mu^T w - lambda * w^T Sigma w`

Equivalent implementation:
- minimize `-(mu^T w - lambda * w^T Sigma w)`

Constraints:
- `sum(w) = 1`
- `w_i >= 0`
- `w_i <= max_asset_weight` if configured
- `mu^T w >= min_return` if configured
- `sqrt(w^T Sigma w) <= max_volatility` if configured

Fallback:
- If SLSQP cannot solve the primary objective, run a minimum-variance optimization under the same allocation constraints where possible.

## Installation

### Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### Quick commands

```bash
make install
make test
make run-api
make run-cli
```

## Examples

### CLI example

```bash
python -m portfolio_optimizer.cli
```

Example output:
```json
{
  "weights": {
    "US Equity": 0.32,
    "International Equity": 0.18,
    "US Bonds": 0.30,
    "Global Bonds": 0.10,
    "Real Assets": 0.10
  }
}
```

### API example

Start server:
```bash
uvicorn portfolio_optimizer.api:app --host 0.0.0.0 --port 8000
```

Health check:
```bash
curl http://localhost:8000/health
```

Optimization request:
```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d @examples/example_request.json
```

### Streamlit example

```bash
streamlit run app/streamlit_app.py
```

## Testing

Run:
```bash
pytest --cov=src/portfolio_optimizer --cov-report=term-missing
```

Tests cover:
- weights sum to one
- allocation constraints
- schema validation for correlation shape
- risk mapping monotonic behavior

## Deployment with Docker / FastAPI

Build image:
```bash
docker build -t customer-portfolio-optimizer .
```

Run container:
```bash
docker run --rm -p 8000:8000 customer-portfolio-optimizer
```

The container launches the FastAPI service via Uvicorn.

## Outcome

This project produces a verifiable GitHub structure that demonstrates:
- optimization fundamentals
- API engineering
- data validation
- deterministic testing
- communication of model outputs to non-technical users

It is useful as a portfolio artifact for analytics, data science, machine learning platform, quantitative product, or backend engineering interviews.

## Interview Talking Points

- Why customer-aware optimization is more useful than pure return maximization
- How to encode business policy as mathematical constraints
- Why deterministic synthetic data is valuable for testing and demos
- Tradeoffs between mean-variance simplicity and production realism
- Why fallback optimization paths improve robustness
- How Pydantic validation prevents malformed requests from reaching core logic
- How to separate schemas, policy mapping, optimization, explanation, and delivery layers
- How this design could evolve toward transaction costs, tax lots, rebalancing bands, or scenario stress testing
- Why this repository is intentionally GitHub-ready and interview-friendly
- How to explain optimizer outputs to product managers, compliance teams, and customers

## Key Files

- `customer-portfolio-optimizer.zip`
- `README.md`
- `src/portfolio_optimizer/optimizer.py`
- `src/portfolio_optimizer/api.py`
- `tests/test_optimizer.py`

## Download Links

When generated in the target environment, these files are available at:
- `/mnt/data/customer-portfolio-optimizer.zip`
- `/mnt/data/customer-portfolio-optimizer/README.md`
- `/mnt/data/customer-portfolio-optimizer/src/portfolio_optimizer/optimizer.py`
- `/mnt/data/customer-portfolio-optimizer/src/portfolio_optimizer/api.py`
- `/mnt/data/customer-portfolio-optimizer/tests/test_optimizer.py`
