import streamlit as st


def show_metrics(results):

    capital = results.final_capital
    profit = results.profit
    trades = results.trades

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Capital",
        f"₹{capital:,.2f}"
    )

    col2.metric(
        "Profit",
        f"₹{profit:,.2f}"
    )

    col3.metric(
        "Trades",
        trades
    )

    col4.metric(
        "Return",
        f"{profit/100000*100:.2f}%"
    )