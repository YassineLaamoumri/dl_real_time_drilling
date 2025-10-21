#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Starting MLflow dev server (file backend, local artifacts)..."
export MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI:-http://127.0.0.1:5000}
mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri ./mlruns --default-artifact-root ./mlruns

