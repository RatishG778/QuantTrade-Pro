import streamlit as st
import pandas as pd


def trade_table(results):

    trade_df = pd.DataFrame({
        "Profit": results.trade_history,
    })

    st.dataframe(
        trade_df,
        use_container_width=True
    )