from research.validation.workflow import ValidationWorkflow
from research.validation.report import ValidationReport

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

ValidationReport.generate(result)