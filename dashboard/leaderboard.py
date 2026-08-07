import streamlit as st

from research.optimization.leaderboard import Leaderboard


def leaderboard_page():

    lb = Leaderboard()

    df = lb.by_profit()

    st.subheader("🏆 Strategy Leaderboard")

    if df.empty:

        st.info("No experiments found.")

        return

    # Ranking

    df.insert(0, "Rank", range(1, len(df) + 1))

    st.dataframe(
        df,
        use_container_width=True
    )

    best = df.iloc[0]

    st.success(
        f"""
🥇 Best Experiment

Strategy : {best['Strategy']}

Profit : ₹{best['Profit']:.2f}

Drawdown : {best['Drawdown']:.2f}

Trades : {best['Trades']}
"""
    )