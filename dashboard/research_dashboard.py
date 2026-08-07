import streamlit as st

from dashboard.experiments import experiment_history
from dashboard.leaderboard import leaderboard_page
from dashboard.heatmap import heatmap_page
from dashboard.portfolio import portfolio_dashboard


def research_dashboard():

    st.title("🧪 Quant Research Dashboard")

    experiment_history()

    st.divider()

    leaderboard_page()

    st.divider()

    heatmap_page()

    st.divider()

    portfolio_dashboard()