import pytest
import pandas as pd


@pytest.fixture
def sample_data():

    return pd.read_csv(
        "data/features/AAPL.csv"
    )


@pytest.fixture
def initial_capital():

    return 100000