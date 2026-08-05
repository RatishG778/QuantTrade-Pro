import plotly.express as px
import pandas as pd


def allocation_chart(allocation):

    df = pd.DataFrame([
        {
            "Stock": symbol,
            "Capital": info["capital"]
        }
        for symbol, info in allocation.items()
    ])

    fig = px.pie(
        df,
        names="Stock",
        values="Capital",
        title="Portfolio Allocation"
    )

    return fig

def performance_chart(results):

    df = pd.DataFrame([
        {
            "Stock": stock,
            "Profit": result["Profit"]
        }
        for stock, result in results.items()
    ])

    fig = px.bar(
        df,
        x="Stock",
        y="Profit",
        title="Stock Profit Comparison"
    )

    return fig