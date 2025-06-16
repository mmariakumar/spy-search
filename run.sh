#!/bin/bash

# Trap SIGINT (Ctrl-C) and SIGTERM to kill child processes
cleanup() {
  echo "Stopping backend and frontend..."
  kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
  exit 1
}
trap cleanup SIGINT SIGTERM

# Check if virtual environment exists and activate it
if [ -d ".venv" ]; then
  echo "Activating virtual environment..."
  . .venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }
else
  echo "Virtual environment not found. Please run the setup script first."
  exit 1
fi

# Check if uvicorn is installed
if ! command -v uvicorn >/dev/null 2>&1; then
  echo "uvicorn not found, installing..."
  uv pip install uvicorn || { echo "Failed to install uvicorn"; exit 1; }
fi

# Start backend
echo "Starting FastAPI backend..."
uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait briefly to ensure backend starts
sleep 2

# Check if backend is running
if ! ps -p $BACKEND_PID >/dev/null; then
  echo "Backend failed to start"
  exit 1
fi

# Start frontend
echo "Starting frontend..."
(
  cd frontend || { echo "Failed to cd to frontend directory"; exit 1; }
  # Install npm dependencies only if node_modules is missing
  if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install --legacy-peer-deps || { echo "npm install failed"; exit 1; }
  else
    echo "npm dependencies already installed"
  fi
  
  # Set environment variables for host binding
  export HOST=0.0.0.0
  export PORT=8080
  
  # Start frontend with host binding (this works for most frameworks)
  npm run dev -- --host 0.0.0.0 --port 8080 2>/dev/null || \
  npm run dev -- -H 0.0.0.0 -p 8080 2>/dev/null || \
  HOST=0.0.0.0 PORT=8080 npm run dev
) &
FRONTEND_PID=$!

# Wait briefly to ensure frontend starts
sleep 2

# Check if frontend is running
if ! ps -p $FRONTEND_PID >/dev/null; then
  echo "Frontend failed to start"
  exit 1
fi

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Backend accessible at: http://localhost:8000"
echo "Frontend accessible at: http://localhost:8080"

# Wait for both processes to exit
wait $BACKEND_PID $FRONTEND_PID