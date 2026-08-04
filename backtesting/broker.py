class Broker:

    def __init__(
        self,
        commission_rate=0.001,
        slippage_rate=0.0005
    ):
        self.commission_rate = commission_rate
        self.slippage_rate = slippage_rate

    def execute_buy(self, price, shares):

        executed_price = price * (1 + self.slippage_rate)

        commission = executed_price * shares * self.commission_rate

        return executed_price, commission

    def execute_sell(self, price, shares):

        executed_price = price * (1 - self.slippage_rate)

        commission = executed_price * shares * self.commission_rate

        return executed_price, commission