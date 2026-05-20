"""Command line interface for running an example optimization."""

from __future__ import annotations

import json

from .data import create_example_request
from .optimizer import optimize_portfolio


def main() -> None:
    request = create_example_request()
    result = optimize_portfolio(request)
    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    main()
