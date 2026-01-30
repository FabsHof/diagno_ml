"""Pytest configuration and shared fixtures for DiagnoML tests."""

from collections.abc import Generator
from typing import Any

import pytest


@pytest.fixture(scope="session")
def test_settings() -> dict[str, Any]:
    """Provide test configuration settings.

    Returns:
        Dictionary with test configuration values.
    """
    return {
        "gcp_project_id": "test-project",
        "bq_dataset": "test_dataset",
        "mlflow_tracking_uri": "http://localhost:5000",
        "api_host": "localhost",
        "api_port": 8000,
    }


@pytest.fixture
def sample_patient_data() -> dict[str, Any]:
    """Provide sample patient data for testing.

    Returns:
        Dictionary with sample patient data matching the minimal dataset schema.
    """
    return {
        "pseudonym": "PID-TEST123456",
        "geschlecht": "m",
        "altersgruppe": "46-60",
        "raucher_status": "ja",
        "raucher_zeitraum_kategorie": "5-15y",
        "raucher_menge_kategorie": "10-20",
        "alkohol_status": "nein",
        "alkohol_zeitraum_kategorie": None,
        "drogen_status": "nein",
        "drogen_zeitraum_kategorie": None,
        "sport_niveau": "wenig",
        "sport_stunden_kategorie": "1-3",
        "hba1c": 5.8,
        "cholesterol_total": 210.0,
        "crp": 2.5,
        "created_at": "2024-01-15T10:30:00Z",
        "data_version": "1.0.0",
    }


@pytest.fixture
def sample_analysis_result() -> dict[str, Any]:
    """Provide sample analysis result for testing.

    Returns:
        Dictionary with sample analysis result.
    """
    return {
        "pseudonym": "PID-TEST123456",
        "diagnosis_probability": 0.73,
        "risk_category": "high",
        "confidence_score": 0.85,
        "model_version": "1.0.0",
        "prediction_timestamp": "2024-01-15T11:00:00Z",
    }


@pytest.fixture(scope="function")
def temp_data_dir(tmp_path: Any) -> Generator[Any, None, None]:
    """Provide a temporary directory for test data.

    Args:
        tmp_path: pytest built-in fixture for temporary paths.

    Yields:
        Path to the temporary directory.
    """
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    yield data_dir


# Markers for test categorization
def pytest_configure(config: Any) -> None:
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "e2e: mark test as end-to-end test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
