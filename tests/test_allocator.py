from core.portfolio_engine.allocator import PortfolioAllocator


def test_allocator():

    allocator = PortfolioAllocator(100000)

    allocation = allocator.equal_weight([
        "AAPL",
        "MSFT"
    ])

    assert allocation["AAPL"]["capital"] == 50000

    assert allocation["MSFT"]["capital"] == 50000