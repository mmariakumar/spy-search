#!/bin/bash

# Start backend
echo "Starting FastAPI backend..."
uvicorn main:app &

BACKEND_PID=$!

sleep 2

# Start frontend
echo "Starting frontend..."
(
  cd frontend || { echo "Failed to cd frontend"; exit 1; }
  echo "Running npm install..."
  npm install
  echo "Running npm run dev..."
  npm run dev
) &

FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"

wait