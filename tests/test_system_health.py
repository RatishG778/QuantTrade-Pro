def test_core_modules_import():

    from core.backtesting.engine import BacktestEngine
    from core.backtesting.portfolio import Portfolio
    from core.backtesting.result import BacktestResult

    from research.experiments.runner import ExperimentRunner
    from research.optimization.optimizer import Optimizer
    from research.validation.walk_forward import WalkForwardValidator

    from research.portfolio.analytics import PortfolioAnalytics
    from research.portfolio.correlation import CorrelationAnalyzer
    from research.portfolio.allocation import AllocationEngine

    from research.monte_carlo.simulator import MonteCarloSimulator
    from research.monte_carlo.report import MonteCarloReport

    from ml.features import FeatureEngineer
    from ml.trainer import MLTrainer
    from ml.evaluator import MLEvaluator

    from research.reports.performance_report import PerformanceReport

    assert BacktestEngine
    assert Portfolio
    assert BacktestResult
    assert ExperimentRunner
    assert Optimizer
    assert WalkForwardValidator
    assert PortfolioAnalytics
    assert CorrelationAnalyzer
    assert AllocationEngine
    assert MonteCarloSimulator
    assert MonteCarloReport
    assert FeatureEngineer
    assert MLTrainer
    assert MLEvaluator
    assert PerformanceReport