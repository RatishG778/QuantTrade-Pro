from research.experiments.experiment import Experiment
from research.experiments.runner import ExperimentRunner

experiment = Experiment(

    name="Moving Average Test",

    strategy="Moving Average",

    symbol="AAPL",

    capital=100000,

    parameters={
        "fast": 20,
        "slow": 50
    }

)

runner = ExperimentRunner()

results = runner.run(experiment)

print(results)