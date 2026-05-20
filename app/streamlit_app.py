from __future__ import annotations

import json
import os
import sys

import streamlit as st

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from portfolio_optimizer.data import create_example_request
from portfolio_optimizer.optimizer import optimize_portfolio

st.set_page_config(page_title="Customer Portfolio Optimizer", layout="centered")
st.title("Customer Portfolio Optimizer")
st.write("Run a deterministic example optimization for a customer-aware portfolio recommendation.")

if st.button("Run Example Optimization"):
    req = create_example_request()
    result = optimize_portfolio(req)
    st.subheader("Optimization Result")
    st.json(result.model_dump())
    st.subheader("Weights")
    st.bar_chart(result.weights)
    st.subheader("Example Request")
    st.code(json.dumps(req.model_dump(), indent=2), language="json")
