from research.monte_carlo.simulator import MonteCarloSimulator

from dashboard.run_backtest import run_backtest


result = run_backtest(

    symbol="AAPL",

    capital=100000,

    strategy_name="Moving Average"

)

sim = MonteCarloSimulator()

profits = sim.simulate(

    result.trade_history,

    simulations=100

)

print("=" * 60)

print("Monte Carlo")

print("=" * 60)

print("Best :", max(profits))

print("Worst:", min(profits))

print("Average:", sum(profits)/len(profits))