import streamlit as st
import pandas as pd


def comparison_table(results):

    df = pd.DataFrame(results)

    st.subheader("Strategy Comparison")

    st.dataframe(
        df,
        use_container_width=True
    )

    best = df.loc[df["Return (%)"].idxmax()]

    st.success(
        f"🏆 Best Strategy : {best['Strategy']}"
    )