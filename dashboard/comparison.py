import streamlit as st
import pandas as pd


def comparison_table(results):

    df = pd.DataFrame(results)

    st.subheader("📊 Strategy Comparison")

    st.dataframe(
        df,
        use_container_width=True
    )

    # Check if dataframe is empty
    if df.empty:
        st.warning("No comparison results available.")
        return

    # Best strategy based on Profit
    best = df.loc[df["Profit"].idxmax()]

    st.success(
        f"""
🏆 Best Strategy: **{best['Strategy']}**

💰 Profit: **₹{best['Profit']:.2f}**

📈 Trades: **{best['Trades']}**

🏦 Final Capital: **₹{best['Final Capital']:.2f}**
"""
    )