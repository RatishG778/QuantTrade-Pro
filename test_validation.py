from research.validation.validator import ValidationEngine

engine = ValidationEngine()

result = engine.validate(

    symbol="AAPL",

    capital=100000,

    strategy="Moving Average",

    parameters={

        "fast":10,

        "slow":60

    }

)

print(result)