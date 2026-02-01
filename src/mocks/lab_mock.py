"""Lab Mock Service - Simulates external laboratory API for development.

This mock service provides synthetic lab results for testing the DiagnoML
pipeline without requiring a real laboratory integration.
"""

import random
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="DiagnoML Lab Mock Service",
    description="Mock laboratory API for development and testing",
    version="1.0.0",
)


class LabRequest(BaseModel):
    """Request model for lab results."""

    patient_id: str = Field(..., description="Patient identifier")
    test_types: list[str] = Field(
        default=["hba1c", "cholesterol", "crp"],
        description="Types of lab tests to request",
    )


class LabResult(BaseModel):
    """Model for a single lab test result."""

    test_type: str
    value: float
    unit: str
    reference_min: float
    reference_max: float
    timestamp: datetime


class LabResponse(BaseModel):
    """Response model for lab results."""

    patient_id: str
    results: list[LabResult]
    lab_id: str
    processed_at: datetime


# Reference ranges for lab tests
LAB_REFERENCE_RANGES: dict[str, dict[str, Any]] = {
    "hba1c": {
        "unit": "%",
        "min": 4.0,
        "max": 5.6,
        "normal_mean": 5.2,
        "normal_std": 0.3,
        "abnormal_mean": 7.5,
        "abnormal_std": 1.5,
    },
    "cholesterol_total": {
        "unit": "mg/dL",
        "min": 0,
        "max": 200,
        "normal_mean": 180,
        "normal_std": 20,
        "abnormal_mean": 260,
        "abnormal_std": 40,
    },
    "cholesterol_ldl": {
        "unit": "mg/dL",
        "min": 0,
        "max": 100,
        "normal_mean": 90,
        "normal_std": 15,
        "abnormal_mean": 150,
        "abnormal_std": 30,
    },
    "cholesterol_hdl": {
        "unit": "mg/dL",
        "min": 40,
        "max": 60,
        "normal_mean": 55,
        "normal_std": 10,
        "abnormal_mean": 35,
        "abnormal_std": 8,
    },
    "crp": {
        "unit": "mg/L",
        "min": 0,
        "max": 3.0,
        "normal_mean": 1.0,
        "normal_std": 0.5,
        "abnormal_mean": 8.0,
        "abnormal_std": 3.0,
    },
    "glucose_fasting": {
        "unit": "mg/dL",
        "min": 70,
        "max": 100,
        "normal_mean": 90,
        "normal_std": 8,
        "abnormal_mean": 140,
        "abnormal_std": 30,
    },
    "triglycerides": {
        "unit": "mg/dL",
        "min": 0,
        "max": 150,
        "normal_mean": 100,
        "normal_std": 25,
        "abnormal_mean": 220,
        "abnormal_std": 50,
    },
}


def generate_lab_value(test_type: str, abnormal_probability: float = 0.3) -> float:
    """Generate a synthetic lab value.

    Args:
        test_type: Type of lab test.
        abnormal_probability: Probability of generating an abnormal value.

    Returns:
        Generated lab value.
    """
    if test_type not in LAB_REFERENCE_RANGES:
        return round(random.uniform(0, 100), 2)

    config = LAB_REFERENCE_RANGES[test_type]
    is_abnormal = random.random() < abnormal_probability

    if is_abnormal:
        value = random.gauss(config["abnormal_mean"], config["abnormal_std"])
    else:
        value = random.gauss(config["normal_mean"], config["normal_std"])

    return round(max(0, value), 2)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        Health status response.
    """
    return {"status": "healthy", "service": "lab-mock"}


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint.

    Returns:
        Service information.
    """
    return {
        "service": "DiagnoML Lab Mock Service",
        "version": "1.0.0",
        "available_tests": list(LAB_REFERENCE_RANGES.keys()),
    }


@app.post("/api/v1/lab/request", response_model=LabResponse)
async def request_lab_results(request: LabRequest) -> LabResponse:
    """Request lab results for a patient.

    Args:
        request: Lab request containing patient ID and test types.

    Returns:
        Lab results response.
    """
    results = []
    for test_type in request.test_types:
        if test_type not in LAB_REFERENCE_RANGES:
            continue

        config = LAB_REFERENCE_RANGES[test_type]
        results.append(
            LabResult(
                test_type=test_type,
                value=generate_lab_value(test_type),
                unit=config["unit"],
                reference_min=config["min"],
                reference_max=config["max"],
                timestamp=datetime.utcnow(),
            )
        )

    if not results:
        raise HTTPException(
            status_code=400,
            detail=f"No valid test types provided. Available: {list(LAB_REFERENCE_RANGES.keys())}",
        )

    return LabResponse(
        patient_id=request.patient_id,
        results=results,
        lab_id=f"LAB-{random.randint(100000, 999999)}",
        processed_at=datetime.utcnow(),
    )


@app.get("/api/v1/lab/results/{patient_id}", response_model=LabResponse)
async def get_lab_results(patient_id: str) -> LabResponse:
    """Get all available lab results for a patient.

    Args:
        patient_id: Patient identifier.

    Returns:
        Lab results response with all available tests.
    """
    results = []
    for test_type, config in LAB_REFERENCE_RANGES.items():
        results.append(
            LabResult(
                test_type=test_type,
                value=generate_lab_value(test_type),
                unit=config["unit"],
                reference_min=config["min"],
                reference_max=config["max"],
                timestamp=datetime.utcnow(),
            )
        )

    return LabResponse(
        patient_id=patient_id,
        results=results,
        lab_id=f"LAB-{random.randint(100000, 999999)}",
        processed_at=datetime.utcnow(),
    )


@app.get("/api/v1/lab/tests")
async def list_available_tests() -> dict[str, Any]:
    """List all available lab tests and their reference ranges.

    Returns:
        Dictionary of available tests with reference ranges.
    """
    return {
        "tests": {
            test_type: {
                "unit": config["unit"],
                "reference_range": {"min": config["min"], "max": config["max"]},
            }
            for test_type, config in LAB_REFERENCE_RANGES.items()
        }
    }
