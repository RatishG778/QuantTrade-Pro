from research.validation.metrics import ValidationMetrics

score = ValidationMetrics.robustness_score(

    walk_forward_pass_rate=0.90,

    monte_carlo_pass_rate=0.85,

    max_drawdown=8

)

print(score)