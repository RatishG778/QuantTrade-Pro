class AllocationEngine:

    @staticmethod
    def best_portfolio(results):

        return max(

            results,

            key=lambda x: x["sharpe"]

        )

    @staticmethod
    def safest_portfolio(results):

        return min(

            results,

            key=lambda x: x["risk"]

        )