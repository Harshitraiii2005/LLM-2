#!/bin/bash

set -e

echo " Installing dependencies..."
pip install --upgrade mlflow prefect

echo "Starting MLflow server on port 5090..."
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 \
  --port 5090 &


echo "Starting Prefect server..."
prefect server start &


echo "Starting Flask app..."
python app.py


