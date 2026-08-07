from research.monte_carlo.metrics import MonteCarloMetrics

profits = [

10000,

15000,

12000,

17000,

9000,

14000,

20000,

16000

]

summary = MonteCarloMetrics.summarize(profits)

for key, value in summary.items():

    print(f"{key}: {value:.2f}")
    