from research.validation.workflow import ValidationWorkflow

workflow = ValidationWorkflow()

result = workflow.run(

    symbol="AAPL",

    strategy="Moving Average",

    capital=100000,

    parameters={

        "fast":10,

        "slow":60

    }

)

print(result)