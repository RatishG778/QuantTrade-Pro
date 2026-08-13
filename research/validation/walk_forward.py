from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass
class WalkForwardResult:
    results: list[dict[str, Any]]

    @property
    def total_profit(self) -> float:
        return sum(
            result["profit"]
            for result in self.results
        )

    @property
    def average_return(self) -> float:
        if not self.results:
            return 0.0

        return sum(
            result["return_pct"]
            for result in self.results
        ) / len(self.results)


class WalkForwardValidator:

    def __init__(
        self,
        train_size: int,
        test_size: int,
        step_size: int | None = None
    ):
        if train_size <= 0:
            raise ValueError("train_size must be positive")

        if test_size <= 0:
            raise ValueError("test_size must be positive")

        self.train_size = train_size
        self.test_size = test_size
        self.step_size = step_size or test_size

    def split(self, data: pd.DataFrame):

        start = 0

        while (
            start
            + self.train_size
            + self.test_size
            <= len(data)
        ):
            train_end = start + self.train_size

            test_end = (
                train_end
                + self.test_size
            )

            train_data = data.iloc[
                start:train_end
            ].copy()

            test_data = data.iloc[
                train_end:test_end
            ].copy()

            yield train_data, test_data

            start += self.step_size

    def run(
        self,
        data: pd.DataFrame,
        evaluator
    ) -> WalkForwardResult:

        results = []

        for window_number, (
            train_data,
            test_data
        ) in enumerate(
            self.split(data),
            start=1
        ):

            result = evaluator(
                train_data,
                test_data
            )

            results.append({
                "window": window_number,
                **result
            })

        return WalkForwardResult(results)