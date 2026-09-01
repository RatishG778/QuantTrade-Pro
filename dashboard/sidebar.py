import streamlit as st
from config.settings import INITIAL_CAPITAL
from config.constants import SYMBOLS, STRATEGIES


def sidebar():
    st.sidebar.title("⚙️ Backtest Settings")

    navigation = st.sidebar.radio(
        "Navigation",
        [
            "Overview & Backtest",
            "Research & Optimization",
            "Monte Carlo Simulation",
            "Portfolio Analytics",
            "ML Research",
            "Experiment History"
        ]
    )

    st.sidebar.divider()

    symbol = st.sidebar.selectbox(
        "Stock",
        SYMBOLS
    )

    initial_capital = st.sidebar.number_input(
        "Initial Capital",
        value=INITIAL_CAPITAL
    )

    risk = st.sidebar.slider(
        "Risk Per Trade (%)",
        1,
        10,
        2
    )

    commission = st.sidebar.slider(
        "Commission (%)",
        0.0,
        1.0,
        0.10
    )

    slippage = st.sidebar.slider(
        "Slippage (%)",
        0.0,
        1.0,
        0.05
    )

    strategy = st.sidebar.selectbox(
        "Strategy",
        STRATEGIES
    )

    compare = st.sidebar.checkbox(
        "Compare All Strategies"
    )

    run = st.sidebar.button("▶ Run Backtest")

    return {
        "navigation": navigation,
        "symbol": symbol,
        "capital": initial_capital,
        "risk": risk,
        "commission": commission,
        "slippage": slippage,
        "strategy": strategy,
        "compare": compare,
        "run": run
    }
