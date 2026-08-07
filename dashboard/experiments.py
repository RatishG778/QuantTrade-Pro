import pandas as pd
import streamlit as st

from research.database.repository import ExperimentRepository


def experiments_history():

    repo = ExperimentRepository()

    rows = repo.get_all()

    columns = [

        "ID",

        "Created",

        "Strategy",

        "Symbol",

        "Capital",

        "Parameters",

        "Profit",

        "Return",

        "Sharpe",

        "Drawdown",

        "Trades",

        "Win Rate"

    ]

    df = pd.DataFrame(

        rows,

        columns=columns

    )

    st.subheader("📚 Experiment History")

    st.dataframe(

        df,

        use_container_width=True

    )
