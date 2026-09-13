from pathlib import Path
import mlflow
import pandas as pd
import joblib
import mlflow.sklearn

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS_PATH = PROJECT_ROOT / "artifacts" / "results_summary.csv"
MODEL_PATH = PROJECT_ROOT / "artifacts" / "final_model.joblib"


def log_final_model_run():
    """Log the final Tuned Random Forest results to MLflow."""

    # Store MLflow tracking data locally inside the project
    mlflow.set_tracking_uri(f"sqlite:///{(PROJECT_ROOT / 'mlflow.db').as_posix()}")

    mlflow.set_experiment("olist-late-delivery")

    results = pd.read_csv(RESULTS_PATH)

    validation_row = results[
        (results["model"] == "Tuned Random Forest")
        & (results["dataset"] == "validation")].iloc[0]

    test_row = results[
        (results["model"] == "Tuned Random Forest")
        & (results["dataset"] == "test")].iloc[0]

    with mlflow.start_run(run_name="tuned-random-forest-registered"):
        mlflow.log_param("model_type", "RandomForestClassifier")
        mlflow.log_param("model_variant", "Tuned Random Forest")

        for metric in ["precision", "recall", "f1", "pr_auc", "roc_auc"]:
            mlflow.log_metric(
                f"validation_{metric}",
                float(validation_row[metric]),)

            mlflow.log_metric(
                f"test_{metric}",
                float(test_row[metric]),)

        mlflow.log_artifact(str(RESULTS_PATH))

        mlflow.log_artifact(
            str(MODEL_PATH),
            artifact_path="model_artifact",)

        model = joblib.load(MODEL_PATH)

        mlflow.sklearn.log_model(
            sk_model=model,
            name="model",
            registered_model_name="olist-late-delivery-model",)

        print("MLflow run logged successfully.")


if __name__ == "__main__":
    log_final_model_run()