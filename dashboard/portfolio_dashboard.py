import streamlit as st

from core.portfolio_engine.loader import PortfolioLoader
from core.portfolio_engine.correlation import CorrelationEngine


def portfolio_dashboard():

    loader = PortfolioLoader()

    portfolio = loader.load([

        "AAPL",
        "MSFT",
        "GOOGL",
        "META",
        "NVDA"

    ])

    engine = CorrelationEngine(portfolio)

    st.subheader("📊 Portfolio Correlation")

    st.dataframe(
        engine.matrix(),
        use_container_width=True
    )

    pair, value = engine.strongest_positive()

    st.success(

        f"Strongest Positive Correlation: {pair[0]} ↔ {pair[1]} ({value:.2f})"

    )

    pair, value = engine.strongest_negative()

    st.info(

        f"Strongest Negative Correlation: {pair[0]} ↔ {pair[1]} ({value:.2f})"

    )