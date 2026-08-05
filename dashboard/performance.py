import streamlit as st


def performance_cards(results):

    trade_history = results["trade_history"]

    wins = len([x for x in trade_history if x > 0])
    losses = len([x for x in trade_history if x < 0])

    win_rate = (
        wins / len(trade_history) * 100
        if trade_history else 0
    )

    gross_profit = sum(x for x in trade_history if x > 0)
    gross_loss = abs(sum(x for x in trade_history if x < 0))

    profit_factor = (
        gross_profit / gross_loss
        if gross_loss > 0 else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Winning Trades", wins)
    c2.metric("Losing Trades", losses)
    c3.metric("Win Rate", f"{win_rate:.2f}%")
    c4.metric("Profit Factor", f"{profit_factor:.2f}")