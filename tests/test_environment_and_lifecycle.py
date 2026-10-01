from backend.app.config import EnvironmentConfig, get_environment_config
from backend.app.services.strategy_lifecycle import StrategyLifecycleService


def test_environment_config_default_is_disabled_live():
    config = EnvironmentConfig()

    assert config.environment == "DEVELOPMENT"
    assert config.live_enabled is False
    assert config.paper_enabled is True


def test_environment_config_can_enable_live_only_explicitly():
    config = EnvironmentConfig(live_enabled=True, environment="LIVE")

    assert config.live_enabled is True
    assert config.environment == "LIVE"


def test_strategy_lifecycle_blocks_activation_in_live_without_readiness():
    config = EnvironmentConfig(live_enabled=False, environment="DEVELOPMENT")
    service = StrategyLifecycleService(config)

    result = service.activate_strategy("strategy-123", "LIVE")

    assert result["approved"] is False
    assert result["status"] == "BLOCKED"
    assert "readiness" in result["reason"].lower()


def test_strategy_lifecycle_allows_paper_activation():
    config = EnvironmentConfig(live_enabled=False, environment="DEVELOPMENT")
    service = StrategyLifecycleService(config)

    result = service.activate_strategy("strategy-123", "PAPER")

    assert result["approved"] is True
    assert result["status"] == "ACTIVE"
    assert result["environment"] == "PAPER"


def test_global_get_environment_config_reads_explicit_values():
    config = get_environment_config(environment="PAPER", live_enabled=False)

    assert config.environment == "PAPER"
    assert config.live_enabled is False
