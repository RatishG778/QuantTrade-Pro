import streamlit as st

from dashboard.experiments import experiments_history
from dashboard.leaderboard import leaderboard_page
from dashboard.heatmap import heatmap_page
from dashboard.portfolio_dashboard import portfolio_dashboard


def research_dashboard():

    st.title("🧪 Quant Research Dashboard")

    experiments_history()

    st.divider()

    leaderboard_page()

    st.divider()

    heatmap_page()

    st.divider()

    portfolio_dashboard()