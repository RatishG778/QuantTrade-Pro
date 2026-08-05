import plotly.express as px
import plotly.graph_objects as go


def equity_curve_chart(equity):

    fig = px.line(
        y=equity,
        title="Portfolio Equity Curve"
    )

    fig.update_layout(
        xaxis_title="Trades",
        yaxis_title="Portfolio Value"
    )

    return fig


def price_chart(df):

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Price"
        )
    )

    buy = df[df["Signal"] == 1]

    sell = df[df["Signal"] == -1]

    fig.add_trace(
        go.Scatter(
            x=buy.index,
            y=buy["Close"],
            mode="markers",
            marker=dict(
                color="green",
                size=10,
                symbol="triangle-up"
            ),
            name="BUY"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=sell.index,
            y=sell["Close"],
            mode="markers",
            marker=dict(
                color="red",
                size=10,
                symbol="triangle-down"
            ),
            name="SELL"
        )
    )

    fig.update_layout(
        title="Trading Signals",
        xaxis_rangeslider_visible=False
    )

    return fig