class RiskManager:

    def __init__(
        self,
        max_position_size=1,
        max_daily_loss=5000
    ):
        self.max_position_size = max_position_size
        self.max_daily_loss = max_daily_loss

    def approve_trade(
        self,
        portfolio
    ):

        if portfolio.position >= self.max_position_size:

            return False

        return True