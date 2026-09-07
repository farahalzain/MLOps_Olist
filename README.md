# Olist Late Delivery Prediction — MLOps Project

## Project Overview

This project builds an end-to-end MLOps system for predicting whether an Olist e-commerce order will be delivered late or on time.

The project started with data ingestion and SQL exploration and is being extended into a production-ready machine learning system with reusable Python modules, automated testing, model and data versioning, an inference API, containerization, and CI/CD.

## Machine Learning Problem

The objective is to predict whether an order will be delivered:

- **Late**
- **On time**

The prediction is made after order approval and before shipping or delivery.

The production system performs inference only. Model training and experimentation remain in the notebooks.

## Repository Structure

```text
MLOps_Olist/
├── app/                  # FastAPI application
├── artifacts/            # Locally generated ML artifacts
├── config/               # Project configuration
│   └── config.yaml
├── data/                 # Data files and DVC-managed data
├── models/               # Model-related storage
├── notebooks/            # Training and experimentation notebooks
├── sql/                  # PostgreSQL setup and queries
├── src/
│   └── olist_ml/         # Reusable ML and inference code
├── tests/                # Automated tests
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Notebooks

The machine learning workflow is organized into six notebooks:

1. `01_read_joins.ipynb` — read and join the source tables.
2. `02_create_labels.ipynb` — create the late-delivery target.
3. `03_split.ipynb` — create temporal train, validation, and test splits.
4. `04_eda.ipynb` — perform exploratory data analysis on training data.
5. `05_features_engineering.ipynb` — build features and fit preprocessing objects.
6. `06_train_tune_evaluate.ipynb` — train, tune, select, and evaluate the final model.

## Configuration

Project settings and artifact paths are stored in:

```text
config/config.yaml
```

The application reads configuration through:

```text
src/olist_ml/config.py
```

This avoids machine-specific absolute paths in the application code.

## Environment Setup

The project uses Python 3.11.

### 1. Create a Virtual Environment

```powershell
python -m venv .venv
```

### 2. Activate the Virtual Environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution for the current session, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Runtime Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Install Development Dependencies

```powershell
python -m pip install -r requirements-dev.txt
```

## Dependencies

Runtime dependencies are pinned in:

```text
requirements.txt
```

Development dependencies are pinned separately in:

```text
requirements-dev.txt
```

This separation keeps production dependencies distinct from tools used for testing, linting, and development.

## Database

The original Olist CSV files were loaded into PostgreSQL using Docker.

The database contains nine main tables:

- `customers`
- `orders`
- `order_items`
- `order_payments`
- `order_reviews`
- `products`
- `sellers`
- `geolocation`
- `category_translation`

The SQL scripts are available in the `sql/` directory:

- `create_tables.sql` — creates the database tables.
- `load_data.sql` — loads the CSV data into PostgreSQL.
- `queries.sql` — contains SQL queries used to inspect and verify the database.

## Dataset

The original CSV files are not stored in Git.

The project uses the Olist Brazilian E-Commerce Public Dataset.

Data and machine learning artifacts will be versioned separately as part of the MLOps workflow.

## Inference Design

The production system is designed for inference on new orders.

The inference workflow will:

1. Receive data for a new order.
2. Validate the input data.
3. Reproduce the same feature engineering used during training.
4. Load the fitted preprocessing artifacts.
5. Transform the new order without refitting preprocessing objects.
6. Load the final trained model.
7. Return the predicted class and late-delivery probability.

Training is not performed during inference.

## Current Status

Task 3 productionization is currently in progress.

Completed so far:

- Repository restructuring
- Notebook organization
- Central configuration
- Portable project paths
- Virtual environment setup
- Runtime dependency pinning
- Development dependency separation
- Initial project documentation

The remaining production components will be documented as they are implemented.