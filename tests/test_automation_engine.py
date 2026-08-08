from automation.automation_engine import AutomationEngine
from automation.config import AutomationConfig

engine = AutomationEngine()

config = AutomationConfig(

    symbols=[

        "AAPL",

        "MSFT"

    ],

    strategies=[

        "Moving Average",

        "RSI"

    ],

    capital=100000

)

results = engine.run(config)

print(f"\nCompleted {len(results)} experiments.")