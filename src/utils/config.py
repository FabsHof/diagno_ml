"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # GCP
    gcp_project_id: str = "diagnoml-poc"
    bq_dataset: str = "diagnoml_warehouse"
    bq_location: str = "EU"
    gcs_bucket: str = "diagnoml-artifacts"

    # OpenClinica
    oc_base_url: str = "http://openclinica:8080/OpenClinica"
    oc_client_id: str = ""
    oc_client_secret: str = ""
    oc_study_oid: str = "S_DIAGNOML"

    # Prefect
    prefect_api_url: str = ""
    prefect_api_key: str = ""

    # MLflow
    mlflow_tracking_uri: str = "http://mlflow:5000"
    mlflow_artifact_root: str = "gs://diagnoml-mlflow-artifacts"
    mlflow_experiment_name: str = "diagnoml-experiments"

    # API
    api_host: str = "0.0.0.0"  # noqa: S104 # nosec B104 - intentional for Docker
    api_port: int = 8000
    api_debug: bool = False

    # Logging
    log_level: str = "INFO"


settings = Settings()
