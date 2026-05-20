PYTHON ?= python

.PHONY: install test run-api run-cli run-ui

install:
	$(PYTHON) -m pip install -e .[dev]

test:
	pytest --cov=src/portfolio_optimizer --cov-report=term-missing

run-api:
	uvicorn portfolio_optimizer.api:app --reload --host 0.0.0.0 --port 8000

run-cli:
	$(PYTHON) -m portfolio_optimizer.cli

run-ui:
	streamlit run app/streamlit_app.py
