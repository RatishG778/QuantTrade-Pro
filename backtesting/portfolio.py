class Portfolio:

    

    def __init__(self, initial_capital):

        self.initial_capital = initial_capital
        self.cash = initial_capital

        self.position = 0
        self.entry_price = None

        self.trade_history = []

    def buy(self, price):

        if self.position == 0:

            self.position = 1
            self.entry_price = price

            print(f"BUY  -> {price:.2f}")

    def sell(self, price):

        if self.position == 1:

            profit = price - self.entry_price

            self.cash += profit

            self.trade_history.append(profit)

            print(
                f"SELL -> {price:.2f} | Profit {profit:.2f}"
            )

            self.position = 0
            self.entry_price = None

    def get_trade_history(self):
        return self.trade_history

    def summary(self):

        print("\n" + "="*50)

        print("Portfolio Summary")

        print("="*50)

        print(f"Initial Capital : {self.initial_capital}")

        print(f"Final Cash      : {self.cash}")

        print(f"Trades          : {len(self.trade_history)}")

        print(f"Total Profit    : {sum(self.trade_history):.2f}")