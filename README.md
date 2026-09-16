# Olist Late Delivery Prediction - MLOps Project

## Project Overview

This project implements an end-to-end MLOps system for predicting whether an Olist e-commerce order will be delivered late or on time.

The project covers the complete workflow from data exploration and feature engineering to model tracking, model serving, automated testing, containerization, continuous integration, and continuous delivery.

## Machine Learning Problem

The objective is to classify an order as:

- **Late**
- **On Time**

The production system performs inference on new orders using the preprocessing artifacts and trained model created during the training workflow.

## MLOps Architecture

```text
Olist Data
    |
    v
PostgreSQL / SQL
    |
    v
Data Preparation & Feature Engineering
    |
    v
Model Training & Evaluation
    |
    v
MLflow Tracking & Model Registry
    |
    v
Registered Model
    |
    v
FastAPI Inference API
    |
    v
Docker / Docker Compose
    |
    +---- PostgreSQL
    +---- MLflow
    +---- FastAPI
    |
    v
GitHub Actions CI/CD
    |
    v
GitHub Container Registry (GHCR)
```

## Repository Structure

```text
MLOps_Olist/
|-- .github/workflows/       # GitHub Actions CI/CD
|-- app/                     # FastAPI application
|-- config/                  # Project configuration
|-- notebooks/               # ML experimentation and training
|-- sql/                     # PostgreSQL scripts
|-- src/olist_ml/            # Reusable ML production code
|-- tests/                   # Automated tests
|-- artifacts.dvc            # DVC artifact tracking
|-- Dockerfile               # FastAPI image
|-- Dockerfile.mlflow        # MLflow image
|-- docker-compose.yml       # Multi-container environment
|-- pytest.ini               # Pytest configuration
|-- requirements.txt         # Runtime dependencies
|-- requirements-dev.txt     # Development dependencies
|-- .env.example             # Environment variable template
`-- README.md
```

## Machine Learning Workflow

The training workflow is organized into six notebooks:

1. `01_read_joins.ipynb` - read and join source tables.
2. `02_create_labels.ipynb` - create the late-delivery target.
3. `03_split.ipynb` - create temporal train, validation, and test splits.
4. `04_eda.ipynb` - exploratory data analysis.
5. `05_features_engineering.ipynb` - feature engineering and fitted preprocessing artifacts.
6. `06_train_tune_evaluate.ipynb` - model training, tuning, evaluation, and selection.

Training and experimentation are separated from production inference.

## Production Inference Pipeline

For a new order, the application performs:

```text
Raw Order
   |
   v
Input Validation
   |
   v
Data Quality Validation
   |
   v
Feature Engineering
   |
   v
Fitted Preprocessing
   |
   v
MLflow Registered Model
   |
   v
Probability + Prediction
```

The preprocessing objects are reused during inference and are never refitted on incoming data.

## API

The model is served through FastAPI.

Main endpoints:

- `GET /health` - API health check.
- `GET /model-info` - registered model information.
- `POST /predict` - prediction for one order.
- `POST /predict-batch` - predictions for multiple orders.

A prediction returns:

- predicted class
- readable label
- late-delivery probability
- model version

## MLflow

MLflow is used for model tracking and model registry.

The inference service loads the registered model using:

```text
models:/olist-late-delivery-model/<version>
```

The MLflow service uses PostgreSQL as its backend store in the Docker Compose environment.

Configuration can be supplied using environment variables such as:

```text
MLFLOW_TRACKING_URI
MLFLOW_MODEL_NAME
MLFLOW_MODEL_VERSION
```

## Docker

The project contains two custom Docker images:

- `Dockerfile` - FastAPI inference service.
- `Dockerfile.mlflow` - MLflow server with PostgreSQL driver support.

Docker Compose coordinates:

```text
PostgreSQL
MLflow
FastAPI
```

Build the services with:

```bash
docker compose build
```

Start the environment with:

```bash
docker compose up -d
```

Check the containers with:

```bash
docker compose ps
```

## Automated Testing

The project includes automated tests for:

- API endpoints
- data quality
- feature engineering
- preprocessing
- input validation
- model inference

Run the complete test suite with:

```bash
python -m pytest -v
```

The current test suite contains **14 automated tests**.

## CI/CD

GitHub Actions runs automatically on pushes and pull requests to `main`.

The pipeline performs:

```text
Checkout Repository
        |
        v
Install Dependencies
        |
        v
Run Automated Tests
        |
        v
Build Docker Compose Services
        |
        v
Generate Docker Metadata
        |
        v
Authenticate with GHCR
        |
        v
Build & Publish API Image
```

Publishing is performed on pushes to `main`.

## GitHub Container Registry

The API Docker image is automatically published to GitHub Container Registry:

```text
ghcr.io/farahalzain/olist-api
```

Published images include:

- `latest`
- a Git commit SHA tag

This provides traceability between source-code revisions and container images.

Example:

```bash
docker pull ghcr.io/farahalzain/olist-api:latest
```

## Configuration and Secrets

Project configuration is stored in:

```text
config/config.yaml
```

Local environment variables are stored in `.env`.

The real `.env` file is excluded from Git. A safe template is provided as:

```text
.env.example
```

Secrets and passwords should never be committed to the repository.

## Technology Stack

- Python 3.11
- pandas
- scikit-learn
- MLflow
- FastAPI
- PostgreSQL
- Docker
- Docker Compose
- DVC
- pytest
- Git / GitHub
- GitHub Actions
- GitHub Container Registry

## Project Status

The end-to-end MLOps workflow is implemented.

Completed components include:

- Data ingestion and SQL exploration
- Feature engineering
- Model training and evaluation
- Reusable production Python modules
- Input and data-quality validation
- Model and preprocessing artifact management
- MLflow tracking and Model Registry
- FastAPI inference service
- Single and batch prediction
- Logging and inference latency monitoring
- Automated testing
- DVC artifact versioning
- Docker containerization
- Docker Compose orchestration
- PostgreSQL-backed MLflow
- GitHub Actions CI
- Automated Docker builds
- Continuous delivery to GHCR
- Versioned container images
- Published-image health validation