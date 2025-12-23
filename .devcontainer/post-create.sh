#!/usr/bin/env bash
set -e
echo "Installing backend deps..."
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt || true
cd ..
echo "Installing frontend deps..."
cd frontend
npm ci || true
cd ..
echo "Done. Use 'docker compose up --build' to run the demo."
