from risk_management.position_sizing import PositionSizing

ps = PositionSizing()

shares = ps.calculate_position_size(
    capital=100000,
    entry_price=200,
    stop_loss=190
)

print(f"Shares to Buy : {shares}")