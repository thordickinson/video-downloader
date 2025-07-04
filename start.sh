#!/bin/bash

echo "Iniciando servidor FastAPI en 0.0.0.0:9000…"
uvicorn app:app --host 0.0.0.0 --port 9000
