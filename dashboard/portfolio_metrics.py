import streamlit as st


def portfolio_summary(summary):

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Portfolio Capital",
        f"₹{summary['Portfolio Capital']:,.2f}"
    )

    c2.metric(
        "Portfolio Profit",
        f"₹{summary['Portfolio Profit']:,.2f}"
    )

    c3.metric(
        "Trades",
        summary["Total Trades"]
    )

    c4, c5 = st.columns(2)

    c4.success(
        f"Best Stock\n\n{summary['Best Stock']}"
    )

    c5.error(
        f"Worst Stock\n\n{summary['Worst Stock']}"
    )