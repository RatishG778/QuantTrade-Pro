from research.validation.validator import ValidationEngine
from research.validation.metrics import ValidationMetrics


class ValidationWorkflow:

    def __init__(self):

        self.validator = ValidationEngine()

    def run(

        self,

        symbol,

        strategy,

        capital,

        parameters

    ):

        validation = self.validator.validate(

            symbol=symbol,

            strategy=strategy,

            capital=capital,

            parameters=parameters

        )

        score = ValidationMetrics.robustness_score(

            walk_forward_pass_rate=1.0 if validation["passed"] else 0.0,

            monte_carlo_pass_rate=1.0,

            max_drawdown=validation["drawdown"]

        )

        validation["robustness"] = score

        return validation