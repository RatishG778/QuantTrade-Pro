import streamlit as st

from dashboard.sidebar import sidebar
from dashboard.metrics import show_metrics
from dashboard.tables import trade_table
from dashboard.charts import price_chart
from dashboard.run_backtest import run_backtest
from dashboard.performance import performance_cards
from dashboard.charts import correlation_heatmap

st.set_page_config(
    page_title="QuantTrade-Pro",
    page_icon="📈",
    layout="wide"
)

st.title("📈 QuantTrade-Pro Dashboard")

settings = sidebar()
if settings["compare"]:

    from dashboard.comparison import comparison_table
    from dashboard.run_backtest import compare_strategies

    comparison = compare_strategies(
        settings["symbol"],
        settings["capital"]
    )

    comparison_table(comparison)

else:
    results = run_backtest(
        settings["symbol"],
        settings["capital"],
        settings["strategy"]
    )
    st.header("Portfolio Overview")

    show_metrics(results)
    st.header("Performance")

    performance_cards(results)

    st.subheader("Equity Curve")

    st.subheader("Price")

    st.subheader("Trading Signals")

    st.subheader("Portfolio Correlation")
    
    fig = correlation_heatmap(correlation_matrix)
    
    st.plotly_chart(fig, use_container_width=True)

    st.plotly_chart(
        price_chart(results["data"]),
        use_container_width=True
) 

    st.subheader("Trade History")

    trade_table(results)