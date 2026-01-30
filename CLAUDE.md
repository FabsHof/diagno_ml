# 🤖 CLAUDE.md - Claude Code Instructions

## Project Overview

**DiagnoML** is a clinical diagnosis prediction PoC that combines:
- Electronic Data Capture (OpenClinica) for patient data management
- Cloud-based ML pipeline (GCP Free Tier) for predictions
- Feedback loop for continuous model improvement

This file provides Claude Code with context for effective assistance.

---

## 🏗️ Architecture & Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| EDC | OpenClinica CE (Docker) | Patient data management |
| Orchestration | Prefect 3.x | Workflow management |
| ML Tracking | MLflow 3.x | Experiment tracking, model registry |
| Data Warehouse | BigQuery (GCP) | Data storage |
| Artifact Storage | Cloud Storage (GCP) | MLflow artifacts |
| Monitoring | Prometheus + Grafana | Metrics & dashboards |
| Drift Detection | Evidently | Data & model drift |
| API | FastAPI | REST endpoints |
| Testing | pytest | Unit & integration tests |
| CI/CD | GitHub Actions | Automation |
| Containerization | Docker Compose | Local deployment |

---

## 📁 Project Structure

```
diagnoml/
├── .github/workflows/       # CI/CD pipelines
├── configs/                 # Service configurations
│   ├── grafana/
│   ├── prometheus/
│   └── openclinica/
├── flows/                   # Prefect flows
│   ├── data_ingestion.py
│   ├── training.py
│   ├── inference.py
│   └── feedback.py
├── src/
│   ├── api/                 # FastAPI application
│   ├── data/
│   │   ├── generators/      # Synthetic data generation
│   │   ├── transformers/    # Data transformations
│   │   └── validators/      # Schema validation
│   ├── edc/                 # EDC integration
│   ├── models/              # ML training & prediction
│   ├── monitoring/          # Observability
│   └── utils/               # Shared utilities
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docker-compose.yml
├── pyproject.toml
└── Makefile
```

---

## 🛠️ Development Commands

```bash
# Setup
uv sync                      # Install dependencies
cp .env.example .env         # Configure environment

# Docker
make build                   # Build all containers
make up                      # Start all services
make down                    # Stop services
make logs                    # Follow logs
make clean                   # Remove volumes

# Development
make test                    # Run all tests
make test-unit               # Run unit tests only
make test-integration        # Run integration tests
make lint                    # Run ruff linter
make format                  # Format code with ruff
make typecheck               # Run mypy

# Prefect
prefect cloud login          # Authenticate to Prefect Cloud
prefect deployment run       # Trigger a flow run

# Demo
make demo                    # Run full demo workflow
make seed                    # Seed synthetic data
```

---

## 🧪 Testing Guidelines

### Test File Naming
- Unit tests: `tests/unit/test_<module>.py`
- Integration tests: `tests/integration/test_<feature>.py`
- E2E tests: `tests/e2e/test_<workflow>.py`

### Test Markers
```python
@pytest.mark.unit           # Fast, isolated tests
@pytest.mark.integration    # Tests with external dependencies
@pytest.mark.e2e            # Full workflow tests
@pytest.mark.slow           # Tests > 10s
```

### Coverage Requirements
- Minimum overall: 80%
- New code: 90%
- Critical paths (models, transformers): 95%

### Test Structure
```python
class TestFeatureName:
    """Test class for feature description."""
    
    @pytest.fixture
    def setup_data(self):
        """Setup test data."""
        return {...}
    
    def test_happy_path(self, setup_data):
        """Test normal operation."""
        # Arrange
        # Act
        # Assert
    
    def test_edge_case(self):
        """Test edge case handling."""
        pass
    
    def test_error_handling(self):
        """Test error scenarios."""
        with pytest.raises(ValueError):
            ...
```

---

## 📝 Code Style Guidelines

### Python Style
- **Formatter**: ruff format (black-compatible)
- **Linter**: ruff
- **Type Checker**: mypy
- **Docstrings**: Google style
- **Max line length**: 88 characters

### Naming Conventions
```python
# Classes: PascalCase
class PatientGenerator:
    pass

# Functions/methods: snake_case
def generate_patient():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRY_ATTEMPTS = 3

# Private: leading underscore
def _internal_helper():
    pass
```

### Import Order
```python
# 1. Standard library
from datetime import datetime
from typing import Dict, List, Optional

# 2. Third-party
import pandas as pd
from prefect import flow, task
from pydantic import BaseModel

# 3. Local application
from src.utils.config import settings
from src.models.train import DiagnosisTrainer
```

### Type Hints
Always use type hints for:
- Function parameters and return types
- Class attributes
- Complex data structures

```python
def process_patient(
    patient_id: str,
    data: Dict[str, Any],
    *,
    validate: bool = True
) -> Optional[PatientResult]:
    """Process patient data.
    
    Args:
        patient_id: Unique patient identifier
        data: Patient data dictionary
        validate: Whether to validate data
        
    Returns:
        Processed patient result or None if invalid
    """
    pass
```

---

## 🔄 CI/CD Pipelines

### PR Checks (`.github/workflows/ci.yml`)
```yaml
triggers: [pull_request]

jobs:
  - lint (ruff check)
  - format (ruff format --check)
  - typecheck (mypy)
  - test-unit (pytest -m unit)
  - test-integration (pytest -m integration)
  - security (bandit)
```

### Main Branch (`.github/workflows/cd.yml`)
```yaml
triggers: [push to main]

jobs:
  - version-bump (semantic-release)
  - build-images
  - push-to-registry
  - deploy-staging (optional)
```

### Versioning
- **Semantic Versioning**: MAJOR.MINOR.PATCH
- **Conventional Commits**:
  - `feat:` → minor bump
  - `fix:` → patch bump
  - `feat!:` or `BREAKING CHANGE:` → major bump

---

## 🔧 Configuration

### Environment Variables
```bash
# GCP
GCP_PROJECT_ID=diagnoml-poc
GOOGLE_APPLICATION_CREDENTIALS=/secrets/gcp-key.json

# OpenClinica
OC_BASE_URL=http://openclinica:8080/OpenClinica
OC_CLIENT_ID=...
OC_CLIENT_SECRET=...
OC_STUDY_OID=S_DIAGNOML

# Prefect
PREFECT_API_URL=https://api.prefect.cloud/api/...
PREFECT_API_KEY=...

# MLflow
MLFLOW_TRACKING_URI=http://mlflow:5000
MLFLOW_ARTIFACT_ROOT=gs://diagnoml-mlflow-artifacts

# Database
BQ_DATASET=diagnoml_warehouse
```

### Config Classes
Use Pydantic Settings for configuration:

```python
# src/utils/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # GCP
    gcp_project_id: str
    
    # OpenClinica
    oc_base_url: str
    oc_client_id: str
    oc_client_secret: str
    
    # MLflow
    mlflow_tracking_uri: str
    
    class Config:
        env_file = ".env"
        
settings = Settings()
```

---

## 🧩 Key Modules

### Data Generators (`src/data/generators/`)
- `PatientGenerator`: Creates synthetic patient data with realistic correlations
- `LabGenerator`: Creates synthetic lab reports

**Usage:**
```python
from src.data.generators.patient_generator import PatientGenerator

gen = PatientGenerator(seed=42)
patients = gen.generate_batch(1000)
```

### Transformers (`src/data/transformers/`)
- `MinimalDatasetTransformer`: Transforms patient data to pseudonymized minimal dataset
- `PseudonymService`: Generates and manages PIDs

### ML Models (`src/models/`)
- `FeatureEngineer`: sklearn preprocessing pipeline
- `DiagnosisTrainer`: Training with hyperparameter tuning
- `DiagnosisPredictor`: Inference with confidence scores

### Prefect Flows (`flows/`)
- `data_ingestion_flow`: EDC → BigQuery
- `training_flow`: BigQuery → Model → MLflow
- `inference_flow`: Model → Predictions
- `feedback_flow`: Feedback → Retraining trigger

---

## 🚨 Common Pitfalls

### 1. MLflow Tracking URI
Always set tracking URI before any MLflow operations:
```python
import mlflow
mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
```

### 2. Prefect Task Retries
Configure retries for external API calls:
```python
@task(retries=3, retry_delay_seconds=60)
async def fetch_data():
    pass
```

### 3. BigQuery Date Handling
Use proper datetime conversion:
```python
from datetime import datetime
# BigQuery expects ISO format
timestamp = datetime.utcnow().isoformat()
```

### 4. Docker Networking
Services communicate via Docker network names, not localhost:
```python
# Correct
MLFLOW_TRACKING_URI = "http://mlflow:5000"

# Wrong (from inside container)
MLFLOW_TRACKING_URI = "http://localhost:5000"
```

---

## 📊 Data Schemas

### Minimal Dataset
```python
{
    "pseudonym": "PID-ABC123DEF456",
    "geschlecht": "m",  # m/w/d
    "altersgruppe": "46-60",  # 18-30, 31-45, 46-60, 61-75, 76+
    "raucher_status": "ja",  # ja/nein/früher
    "raucher_zeitraum_kategorie": "5-15y",  # <5y, 5-15y, >15y
    "raucher_menge_kategorie": "10-20",  # <10, 10-20, >20
    "alkohol_status": "nein",
    "alkohol_zeitraum_kategorie": null,
    "drogen_status": "nein",
    "drogen_zeitraum_kategorie": null,
    "sport_niveau": "wenig",  # viel/wenig/keine
    "sport_stunden_kategorie": "1-3",  # 0, 1-3, 4-7, >7
    "hba1c": 5.8,
    "cholesterol_total": 210.0,
    "crp": 2.5,
    "created_at": "2024-01-15T10:30:00Z",
    "data_version": "1.0.0"
}
```

### Analysis Result
```python
{
    "pseudonym": "PID-ABC123DEF456",
    "diagnosis_probability": 0.73,
    "risk_category": "high",  # low (<0.3), medium (0.3-0.7), high (>0.7)
    "confidence_score": 0.85,
    "model_version": "1.2.0",
    "prediction_timestamp": "2024-01-15T11:00:00Z"
}
```

---

## 🆘 Troubleshooting

### "MLflow server not reachable"
```bash
# Check if container is running
docker ps | grep mlflow

# Check logs
docker logs mlflow

# Verify network
docker network inspect diagnoml_default
```

### "BigQuery permission denied"
```bash
# Verify credentials
gcloud auth application-default print-access-token

# Check service account permissions
gcloud projects get-iam-policy $PROJECT_ID
```

### "Prefect flow not appearing"
```bash
# Re-authenticate
prefect cloud login

# Check deployment
prefect deployment ls
```

---

## 🎯 Quick Reference

### Create New Feature
1. Create feature branch: `git checkout -b feat/my-feature`
2. Implement with tests
3. Run `make lint test`
4. Create PR with conventional commit title

### Add New Prefect Flow
1. Create flow in `flows/my_flow.py`
2. Add deployment in `prefect.yaml`
3. Deploy: `prefect deploy --name my-flow`

### Add New API Endpoint
1. Create route in `src/api/routes/`
2. Add Pydantic schemas in `src/api/schemas.py`
3. Write tests in `tests/unit/test_api.py`
4. Update OpenAPI docs

---

## 📚 Reference Projects

- **oct25_bmlops_int_accidents**: MLOps project with similar architecture (Airflow-based)
- Adapt patterns for Prefect 3.x and GCP Free Tier

---

## 🤝 AI Assistant Guidelines

When helping with this project:

1. **Always consider the full stack** - Changes may affect EDC, pipelines, and cloud components
2. **Write tests first** - TDD approach preferred
3. **Use type hints** - Full typing for all new code
4. **Document decisions** - Add ADRs for architectural choices
5. **Keep costs in mind** - GCP Free Tier limits
6. **Security first** - Pseudonymization is critical
7. **Check existing patterns** - Reuse established patterns from the codebase