#!/bin/sh

# Check if uv is installed
command_exists() {
  command -v "$1" > /dev/null 2>&1
}

if command_exists uv; then
  echo "uv is installed"
else
  echo "uv not found, installing uv..."
  pip install uv
  if [ $? -ne 0 ]; then
    echo "Failed to install uv"
    exit 1
  fi
fi

# Remove any existing virtual environment to avoid conflicts
if [ -d ".venv" ]; then
  echo "Removing existing virtual environment..."
  rm -rf .venv
fi

# Create a fresh virtual environment
echo "Creating virtual environment..."
uv venv
if [ $? -ne 0 ]; then
  echo "Failed to create virtual environment"
  exit 1
fi

# Activate the virtual environment
echo "Activating virtual environment..."
. .venv/bin/activate
if [ $? -ne 0 ]; then
  echo "Failed to activate virtual environment"
  exit 1
fi
echo "Virtual environment activated"

# Install uvicorn and other requirements
echo "Installing uvicorn..."
uv pip install uvicorn
if [ $? -ne 0 ]; then
  echo "Failed to install uvicorn"
  exit 1
fi

echo "Installing requirements..."
uv pip install -r requirements.txt
if [ $? -ne 0 ]; then
  echo "Failed to install requirements"
  exit 1
fi

# Install playwright browsers
echo "Installing playwright browsers..."
playwright install
if [ $? -ne 0 ]; then
  echo "Failed to install playwright browsers"
  exit 1
fi

# Navigate to frontend directory and install npm dependencies
echo "Installing frontend dependencies..."
cd frontend
if [ $? -ne 0 ]; then
  echo "Failed to enter frontend directory"
  exit 1
fi
npm install --legacy-peer-deps
if [ $? -ne 0 ]; then
  echo "npm install failed"
  exit 1
fi

echo "Installation completed successfully!"