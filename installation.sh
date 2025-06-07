#!/bin/sh

python setup.py
# Function to check if a command exists
command_exists() {
  command -v "$1" > /dev/null 2>&1
}

# Check if uv is installed
if command_exists uv; then
  echo "uv is installed, running uv pip install..."
else
  echo "uv not found, installing uv..."
  pip install uv || { echo "Failed to install uv"; exit 1; }
fi

# Use uv to install Python requirements
uv pip install -r requirements.txt || { echo "uv pip install failed"; exit 1; }

# Change directory to frontend
cd frontend || { echo "Failed to enter frontend directory"; exit 1; }

# Run npm install
npm install || { echo "npm install failed"; exit 1; }