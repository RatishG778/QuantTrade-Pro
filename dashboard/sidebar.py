import streamlit as st


def sidebar():

    st.sidebar.title("⚙ Backtest Settings")

    symbol = st.sidebar.selectbox(
        "Stock",
        [
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "META",
            "NVDA",
            "TSLA"
        ]
    )

    initial_capital = st.sidebar.number_input(
        "Initial Capital",
        value=100000
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
    [
        "Moving Average",
        "RSI",
        "MACD"
    ]
)
    compare = st.sidebar.checkbox(
    "Compare All Strategies"
)

    run = st.sidebar.button("▶ Run Backtest")

    return {
        "symbol": symbol,
        "capital": initial_capital,
        "risk": risk,
        "commission": commission,
        "slippage": slippage,
        "strategy": strategy,
        "compare": compare,
        "run": run
    }