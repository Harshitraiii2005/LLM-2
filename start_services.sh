#!/bin/bash

set -e  # Exit immediately if a command fails

echo "Installing dependencies..."
pip install --upgrade mlflow prefect

echo "Starting MLflow server on port 5090..."
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 \
  --port 5090 &

MLFLOW_PID=$!

echo "Starting Prefect server..."
prefect server start &
PREFECT_PID=$!

echo "Running flow.py..."
if python flow.py; then
    echo "flow.py executed successfully."
else
    echo " flow.py failed! Check logs above for errors."
    # Kill background services if flow.py fails
    kill $MLFLOW_PID $PREFECT_PID
    exit 1
fi

echo "All services started successfully."
# Keep script running if needed, or exit safely
wait $MLFLOW_PID $PREFECT_PID
