# 🏥 DiagnoML - Clinical Diagnosis Prediction PoC

## 📋 Projektübersicht

Ein End-to-End MLOps-System zur Vorhersage von Diagnosewahrscheinlichkeiten basierend auf Patientendaten und Laborergebnissen.

### 🎯 Projektziel
Aufbau eines PoC für ein klinisches Entscheidungsunterstützungssystem, das:
- Patientendaten pseudonymisiert verarbeitet
- Laborergebnisse integriert
- ML-basierte Diagnosewahrscheinlichkeiten berechnet
- Feedback-Loop für kontinuierliches Lernen ermöglicht

---

## 🏗️ Architektur-Übersicht

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        GESUNDHEITSVERSORGUNG (On-Premise)                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   👤 Patient ◄──────────────────────────────────────────────┐               │
│       │                                                     │               │
│       │ Einwilligung                                        │ Report        │
│       ▼                                                     │               │
│   👨‍⚕️ Arzt ──────► Anamnese & ──────────────────────────────┼──────────┐    │
│       │           Patientendaten                            │          │    │
│       │                                                     │          │    │
│       ▼                                                     │          │    │
│   ┌─────────────────────────────────────────────────────────┴──────────┤    │
│   │                        EDC (OpenClinica)                           │    │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │    │
│   │  │ Patient-     │  │ Pseudonym-   │  │ Report Generator &       │  │    │
│   │  │ verwaltung   │  │ Generator    │  │ Email Notifications      │  │    │
│   │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │    │
│   │                                                                     │    │
│   │  ┌──────────────────────────────────────────────────────────────┐  │    │
│   │  │                      REST API Interface                       │  │    │
│   │  └──────────────────────────────────────────────────────────────┘  │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
│       │                 ▲                    │                               │
│       │ PID             │ Report & PID       │ Minimaldatensatz & PID       │
│       ▼                 │                    ▼                               │
│   🔬 Externes Labor ────┘                                                   │
│   (Mock für PoC)                                                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                               │
                                               │ HTTPS / REST API
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          GOOGLE CLOUD (Free Tier)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    Prefect Cloud (Orchestration)                     │   │
│   │  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────┐ │   │
│   │  │ Data Ingestion │  │ ML Training    │  │ Inference Pipeline     │ │   │
│   │  │ Flow           │  │ Flow           │  │ Flow                   │ │   │
│   │  └────────────────┘  └────────────────┘  └────────────────────────┘ │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   ┌──────────────────┐  ┌──────────────────┐  ┌────────────────────────┐   │
│   │   BigQuery       │  │   Cloud Storage  │  │   Vertex AI            │   │
│   │   (Data          │  │   (MLflow        │  │   (Training            │   │
│   │   Warehouse)     │  │   Artifacts)     │  │   Compute)             │   │
│   └──────────────────┘  └──────────────────┘  └────────────────────────┘   │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                         Monitoring Stack                             │   │
│   │  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────┐ │   │
│   │  │ Prometheus     │  │ Grafana        │  │ Evidently              │ │   │
│   │  │ (Metrics)      │  │ (Dashboards)   │  │ (Drift Monitoring)     │ │   │
│   │  └────────────────┘  └────────────────┘  └────────────────────────┘ │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                         MLflow (Model Registry)                      │   │
│   │  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────┐ │   │
│   │  │ Experiment     │  │ Model          │  │ Artifact               │ │   │
│   │  │ Tracking       │  │ Registry       │  │ Storage                │ │   │
│   │  └────────────────┘  └────────────────┘  └────────────────────────┘ │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Datenmodell

### Patientendaten (EDC - vollständig)
```yaml
patient_data:
  patient_id: UUID          # Interner Identifier (nie extern sichtbar)
  pseudonym: string         # PID für externe Kommunikation
  
  # Stammdaten
  vorname: string
  nachname: string
  geburtsdatum: date
  geschlecht: enum[männlich, weiblich, divers]
  
  # Kontakt
  email: string
  telefon: string
  adresse: object
  
  # Einwilligung
  consent_date: datetime
  consent_document: blob
  
  # Anamnese (Arzt-Eingabe)
  anamnese:
    raucher_status: enum[ja, nein, früher]
    raucher_zeitraum_jahre: int | null
    raucher_menge_pro_tag: int | null      # Zigaretten
    
    alkohol_status: enum[ja, nein, früher]
    alkohol_zeitraum_jahre: int | null
    
    drogen_status: enum[ja, nein, früher]
    drogen_zeitraum_jahre: int | null
    
    sport_niveau: enum[viel, wenig, keine]
    sport_stunden_pro_woche: float | null
    
    vorerkrankungen: list[string]
    medikamente: list[string]
    allergien: list[string]
```

### Labordaten (vom externen Labor)
```yaml
lab_report:
  pseudonym: string         # PID
  report_date: datetime
  
  # Beispiel-Labormesswerte
  hba1c: float              # Langzeit-Blutzucker (%)
  cholesterol_total: float  # Gesamtcholesterin (mg/dL)
  crp: float                # C-reaktives Protein (mg/L)
  
  # Zusätzliche Werte (erweiterbar)
  additional_values: dict
```

### Minimaldatensatz (pseudonymisiert → Cloud)
```yaml
minimal_dataset:
  pseudonym: string                          # PID als Identifier
  
  # Transformierte demografische Daten
  geschlecht: enum[m, w, d]
  altersgruppe: enum[18-30, 31-45, 46-60, 61-75, 76+]
  
  # Lifestyle-Faktoren (kategorisiert)
  raucher:
    status: enum[ja, nein, früher]
    zeitraum_kategorie: enum[<5y, 5-15y, >15y] | null
    menge_kategorie: enum[<10, 10-20, >20] | null
  
  alkohol:
    status: enum[ja, nein, früher]
    zeitraum_kategorie: enum[<5y, 5-15y, >15y] | null
  
  drogen:
    status: enum[ja, nein, früher]
    zeitraum_kategorie: enum[<5y, 5-15y, >15y] | null
  
  sport:
    niveau: enum[viel, wenig, keine]
    stunden_kategorie: enum[0, 1-3, 4-7, >7] | null
  
  # Labormesswerte (3 ausgewählte)
  hba1c: float
  cholesterol_total: float
  crp: float
  
  # Metadaten
  created_at: datetime
  data_version: string
```

### Analyseergebnis (Cloud → EDC)
```yaml
analysis_result:
  pseudonym: string
  
  # Modell-Vorhersage
  diagnosis_probability: float      # 0.0 - 1.0
  risk_category: enum[low, medium, high]
  confidence_score: float
  
  # Modell-Metadaten
  model_version: string
  prediction_timestamp: datetime
  
  # Feature Importance (Top 5)
  feature_contributions: list[object]
```

### Feedback-Daten (für Retraining)
```yaml
feedback_data:
  pseudonym: string
  
  # Tatsächliches Ergebnis nach Untersuchung
  actual_diagnosis: bool            # True = positiv
  diagnosis_date: datetime
  diagnosis_method: string          # z.B. "Biopsie", "MRT"
  
  # Für Model-Evaluation
  feedback_timestamp: datetime
  submitted_by: string              # Arzt-ID
```

---

## 🚀 Meilensteine

### 📍 Milestone 1: Projekt-Setup & Infrastruktur
**Ziel:** Grundlegende Entwicklungsumgebung und Cloud-Infrastruktur
**Dauer:** ~1 Woche

| Issue | Priorität | Größe |
|-------|-----------|-------|
| M1-01: Repository Setup | P1 | S |
| M1-02: Docker Compose Grundstruktur | P1 | M |
| M1-03: GCP Free Tier Setup | P1 | M |
| M1-04: Prefect Cloud Setup | P1 | S |
| M1-05: MLflow Setup mit GCS Backend | P1 | M |

### 📍 Milestone 2: EDC System
**Ziel:** Funktionierendes OpenClinica mit Formularen
**Dauer:** ~1.5 Wochen

| Issue | Priorität | Größe |
|-------|-----------|-------|
| M2-01: OpenClinica Docker Deployment | P1 | M |
| M2-02: Study Design & CRF Definition | P1 | L |
| M2-03: Pseudonymisierungs-Service | P1 | M |
| M2-04: REST API Integration | P2 | M |
| M2-05: Email Notification Setup | P2 | S |

### 📍 Milestone 3: Synthetische Daten & Labor-Mock
**Ziel:** Realistische Testdaten und Labor-Simulation
**Dauer:** ~1 Woche

| Issue | Priorität | Größe |
|-------|-----------|-------|
| M3-01: Synthetischer Daten-Generator | P1 | L |
| M3-02: Labor-Mock Service | P1 | M |
| M3-03: Daten-Validierung & Schema-Tests | P1 | M |

### 📍 Milestone 4: Data Pipeline (ETL)
**Ziel:** Datenfluss vom EDC zum Data Warehouse
**Dauer:** ~1 Woche

| Issue | Priorität | Größe |
|-------|-----------|-------|
| M4-01: BigQuery Schema & Setup | P1 | M |
| M4-02: Prefect Data Ingestion Flow | P1 | L |
| M4-03: Data Transformation Pipeline | P1 | M |
| M4-04: Data Quality Checks | P2 | M |

### 📍 Milestone 5: ML Training Pipeline
**Ziel:** Trainiertes Logistic Regression Modell
**Dauer:** ~1.5 Wochen

| Issue | Priorität | Größe |
|-------|-----------|-------|
| M5-01: Feature Engineering Module | P1 | M |
| M5-02: Logistic Regression Training | P1 | M |
| M5-03: MLflow Experiment Tracking | P1 | M |
| M5-04: Model Registry & Versioning | P1 | M |
| M5-05: Hyperparameter Tuning | P2 | M |

### 📍 Milestone 6: Inference & Feedback Pipeline
**Ziel:** Vorhersagen und Feedback-Loop
**Dauer:** ~1 Woche

| Issue | Priorität | Größe |
|-------|-----------|-------|
| M6-01: Inference Pipeline | P1 | M |
| M6-02: Result-to-EDC Integration | P1 | M |
| M6-03: Feedback Collection Flow | P1 | M |
| M6-04: Automated Retraining Trigger | P2 | M |

### 📍 Milestone 7: Monitoring & Observability
**Ziel:** Vollständiges Monitoring-Stack
**Dauer:** ~1 Woche

| Issue | Priorität | Größe |
|-------|-----------|-------|
| M7-01: Prometheus Metrics Setup | P1 | M |
| M7-02: Grafana Dashboards | P1 | M |
| M7-03: Evidently Drift Monitoring | P1 | M |
| M7-04: Alerting Rules | P2 | S |

### 📍 Milestone 8: Integration & Testing
**Ziel:** End-to-End funktionierendes System
**Dauer:** ~1 Woche

| Issue | Priorität | Größe |
|-------|-----------|-------|
| M8-01: E2E Integration Tests | P1 | L |
| M8-02: Load Testing | P2 | M |
| M8-03: Documentation | P1 | M |
| M8-04: Demo Workflow | P1 | S |

---

## 📁 Projektstruktur

```
diagnoml/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                 # Linting, Tests
│   │   ├── cd.yml                 # Deployment
│   │   └── version.yml            # Semantic Versioning
│   └── ISSUE_TEMPLATE/
│       └── feature.md
│
├── CLAUDE.md                      # Claude Code Instructions
├── README.md
├── pyproject.toml
├── Makefile
├── docker-compose.yml
├── docker-compose.override.yml    # Local dev overrides
│
├── .env.example
├── .pre-commit-config.yaml
│
├── configs/
│   ├── grafana/
│   │   ├── provisioning/
│   │   └── dashboards/
│   ├── prometheus/
│   │   └── prometheus.yml
│   └── openclinica/
│       └── study_config.xml
│
├── data/
│   ├── raw/                       # Von Generatoren
│   ├── processed/                 # Transformiert
│   └── synthetic/                 # Synthetische Testdaten
│
├── flows/                         # Prefect Flows
│   ├── __init__.py
│   ├── data_ingestion.py
│   ├── training.py
│   ├── inference.py
│   └── feedback.py
│
├── src/
│   ├── __init__.py
│   ├── api/                       # REST API (FastAPI)
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes/
│   │   └── schemas.py
│   │
│   ├── data/                      # Data Processing
│   │   ├── __init__.py
│   │   ├── generators/            # Synthetische Daten
│   │   │   ├── patient_generator.py
│   │   │   └── lab_generator.py
│   │   ├── transformers/
│   │   │   ├── pseudonymizer.py
│   │   │   └── minimal_dataset.py
│   │   └── validators/
│   │       └── schema_validator.py
│   │
│   ├── edc/                       # EDC Integration
│   │   ├── __init__.py
│   │   ├── openclinica_client.py
│   │   └── lab_mock.py
│   │
│   ├── models/                    # ML Models
│   │   ├── __init__.py
│   │   ├── train.py
│   │   ├── predict.py
│   │   ├── evaluate.py
│   │   └── feature_engineering.py
│   │
│   ├── monitoring/                # Observability
│   │   ├── __init__.py
│   │   ├── drift_detector.py
│   │   ├── metrics.py
│   │   └── alerts.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       ├── logging.py
│       └── database.py
│
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_generators.py
│   │   ├── test_transformers.py
│   │   ├── test_models.py
│   │   └── test_api.py
│   ├── integration/
│   │   ├── test_data_pipeline.py
│   │   ├── test_training_pipeline.py
│   │   └── test_edc_integration.py
│   └── e2e/
│       └── test_full_workflow.py
│
├── notebooks/                     # Exploration
│   ├── 01_data_exploration.ipynb
│   └── 02_model_experiments.ipynb
│
├── scripts/
│   ├── setup_gcp.sh
│   ├── seed_data.py
│   └── run_demo.py
│
└── terraform/                     # (Optional) IaC
    ├── main.tf
    ├── bigquery.tf
    └── storage.tf
```

---

## 🛠️ Tech Stack

| Komponente | Technologie | Zweck |
|------------|-------------|-------|
| **EDC** | OpenClinica CE | Patientendaten-Management |
| **Orchestration** | Prefect | Workflow-Management |
| **ML Tracking** | MLflow | Experiment Tracking, Model Registry |
| **Data Warehouse** | BigQuery (GCP) | Datenspeicherung |
| **Artifact Storage** | Cloud Storage (GCP) | MLflow Artifacts |
| **Training Compute** | Vertex AI (GCP) | Model Training |
| **Monitoring** | Prometheus + Grafana | Metriken & Dashboards |
| **Drift Detection** | Evidently | Data & Model Drift |
| **API** | FastAPI | REST Endpoints |
| **Testing** | pytest | Unit & Integration Tests |
| **CI/CD** | GitHub Actions | Automation |
| **Containerization** | Docker + Compose | Deployment |

---

## 📏 Size Estimation Guide

| Size | Beschreibung | Geschätzte Zeit |
|------|--------------|-----------------|
| **S** | Einfache Konfiguration, kleine Änderung | 2-4 Stunden |
| **M** | Neues Feature, mittlere Komplexität | 1-2 Tage |
| **L** | Komplexes Feature, mehrere Komponenten | 3-5 Tage |
| **XL** | Sehr komplex, Research nötig | 1+ Woche |