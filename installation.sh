#!/bin/sh

python setup.py

command_exists() {
  command -v "$1" > /dev/null 2>&1
}

# Check if uvicorn is installed
if command_exists uv; then
  echo "uv is installed, running uv pip install..."
else
  echo "uv not found, installing uv..."
  pip install uv || { echo "Failed to install uvicorn"; exit 1; }
fi

# Use pip to install requirements (uvicorn is already installed if needed)
uv pip install uvicorn

uv pip install -r requirements.txt || { echo "uv pip install failed"; exit 1; }

cd frontend || { echo "Failed to enter frontend directory"; exit 1; }

npm install --legacy-peer-deps || { echo "npm install failed"; exit 1; }