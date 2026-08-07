from core.workflow.pipeline import ResearchPipeline

pipeline = ResearchPipeline()

result = pipeline.execute(

    symbol="AAPL",

    strategy="Moving Average",

    capital=100000,

    parameters={

        "fast":10,

        "slow":60

    }

)

print(result)