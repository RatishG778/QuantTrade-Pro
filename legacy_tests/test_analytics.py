from backtesting.analytics import Analytics

equity = [
    100000,
    103000,
    101000,
    104000,
    99000,
    108000
]

analytics = Analytics(equity)

print("Maximum Drawdown")
print(f"{analytics.max_drawdown():.2f}%")