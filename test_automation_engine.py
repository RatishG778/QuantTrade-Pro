from automation.automation_engine import AutomationEngine

engine = AutomationEngine()

results = engine.run(

    symbols=[

        "AAPL",

        "MSFT",

        "GOOGL"

    ],

    strategies=[

        "Moving Average",

        "RSI",

        "MACD"

    ],

    capital=100000

)

print(len(results))