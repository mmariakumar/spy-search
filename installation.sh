#!/bin/sh

python setup.py

command_exists() {
  command -v "$1" > /dev/null 2>&1
}

# Check if uvicorn is installed
if command_exists uvicorn; then
  echo "uvicorn is installed, running uvicorn pip install..."
else
  echo "uvicorn not found, installing uvicorn..."
  pip install uvicorn || { echo "Failed to install uvicorn"; exit 1; }
fi

# Use pip to install requirements (uvicorn is already installed if needed)
pip install -r requirements.txt || { echo "pip install failed"; exit 1; }

cd frontend || { echo "Failed to enter frontend directory"; exit 1; }

npm install || { echo "npm install failed"; exit 1; }