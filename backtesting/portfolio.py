class Portfolio:

    

    def __init__(self, initial_capital):

        self.initial_capital = initial_capital
        self.cash = initial_capital

        self.position = 0
        self.entry_price = None

        self.trade_history = []


    def buy(self, price,shares):

     if self.position == 0:

        cost = price * shares

        if self.cash >= cost:

            self.cash -= cost

            self.position = shares

            self.entry_price = price

            print("=" * 50)
            print("BUY ORDER")
            print("=" * 50)
            print(f"Price          : {price:.2f}")
            print(f"Shares         : {shares}")
            print(f"Trade Value    : {cost:.2f}")
            print(f"Remaining Cash : {self.cash:.2f}")

    def sell(self, price):

       if self.position > 0:

        proceeds = price * self.position

        cost = self.entry_price * self.position

        profit = proceeds - cost

        self.cash += proceeds

        self.trade_history.append(profit)

        print("=" * 50)
        print("SELL ORDER")
        print("=" * 50)
        print(f"Price          : {price:.2f}")
        print(f"Shares         : {self.position}")
        print(f"Trade Value    : {proceeds:.2f}")
        print(f"Profit         : {profit:.2f}")
        print(f"Cash Balance   : {self.cash:.2f}")

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