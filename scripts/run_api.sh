#!/usr/bin/env bash
set -euo pipefail

export UVICORN_HOST=${UVICORN_HOST:-0.0.0.0}
export UVICORN_PORT=${UVICORN_PORT:-8000}

echo "🚀 Starting API on $UVICORN_HOST:$UVICORN_PORT"
uvicorn src.serving.api:app --host "$UVICORN_HOST" --port "$UVICORN_PORT"

