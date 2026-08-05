class PositionSizing:

    def __init__(self, risk_percent=0.01):
        self.risk_percent = risk_percent

    def calculate_position_size(
        self,
        capital,
        entry_price,
        stop_loss
    ):

        risk_amount = capital * self.risk_percent

        risk_per_share = abs(entry_price - stop_loss)

        if risk_per_share == 0:
            return 0

        shares = int(risk_amount / risk_per_share)

        return shares