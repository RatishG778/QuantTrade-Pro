import pandas as pd


class AllocationEngine:

    @staticmethod
    def equal_weight(
        assets
    ) -> dict:

        assets = list(assets)

        if not assets:
            return {}

        weight = 1.0 / len(assets)

        return {
            asset: weight
            for asset in assets
        }

    @staticmethod
    def normalize(
        weights: dict
    ) -> dict:

        if not weights:
            return {}

        total = sum(weights.values())

        if total == 0:
            return {
                asset: 0.0
                for asset in weights
            }

        return {
            asset: weight / total
            for asset, weight in weights.items()
        }

    @staticmethod
    def portfolio_returns(
        returns: pd.DataFrame,
        weights: dict
    ) -> pd.Series:

        normalized = AllocationEngine.normalize(
            weights
        )

        if not normalized:
            return pd.Series(dtype=float)

        available = [
            asset
            for asset in normalized
            if asset in returns.columns
        ]

        if not available:
            return pd.Series(dtype=float)

        weighted = returns[available].copy()

        for asset in available:
            weighted[asset] *= normalized[asset]

        return weighted.sum(axis=1)