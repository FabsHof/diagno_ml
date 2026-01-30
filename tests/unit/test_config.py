"""Unit tests for configuration module."""

import pytest

from src.utils.config import Settings


@pytest.mark.unit
class TestSettings:
    """Test cases for Settings configuration class."""

    def test_default_settings(self) -> None:
        """Test that default settings are loaded correctly."""
        settings = Settings()

        assert settings.gcp_project_id == "diagnoml-poc"
        assert settings.bq_dataset == "diagnoml_warehouse"
        assert settings.api_port == 8000

    def test_settings_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that settings can be overridden from environment variables."""
        monkeypatch.setenv("GCP_PROJECT_ID", "test-project")
        monkeypatch.setenv("API_PORT", "9000")

        settings = Settings()

        assert settings.gcp_project_id == "test-project"
        assert settings.api_port == 9000

    def test_settings_log_level_default(self) -> None:
        """Test that log level defaults to INFO."""
        settings = Settings()

        assert settings.log_level == "INFO"
