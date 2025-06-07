#!/bin/bash

# Trap SIGINT (Ctrl-C) and SIGTERM to kill child processes
cleanup() {
  echo "Stopping backend and frontend..."
  kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
  exit 1
}

trap cleanup SIGINT SIGTERM

# Start backend
echo "Starting FastAPI backend..."
uvicorn main:app &
BACKEND_PID=$!

sleep 2

# Start frontend
echo "Starting frontend..."
(
  cd frontend || { echo "Failed to cd frontend"; exit 1; }
  npm install
  npm run dev
) &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"

# Wait for both processes to exit
wait $BACKEND_PID $FRONTEND_PID