from research.experiments.runner import ExperimentRunner

runner = ExperimentRunner()

runner.run(

    strategy="Moving Average",

    symbol="AAPL",

    capital=100000,

    parameters={

        "fast": 20,

        "slow": 50

    }

)

print("Experiment saved successfully!")