class ValidationMetrics:

    @staticmethod
    def robustness_score(

        walk_forward_pass_rate,

        monte_carlo_pass_rate,

        max_drawdown

    ):

        score = (

            walk_forward_pass_rate * 40 +

            monte_carlo_pass_rate * 40 +

            max(0, 20 - max_drawdown)

        )

        return round(score, 2)