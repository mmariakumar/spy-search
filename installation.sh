#!/bin/sh

# Check if uv is installed
command_exists() {
  command -v "$1" > /dev/null 2>&1
}

if command_exists uv; then
  echo "uv is installed"
else
  echo "uv not found, installing uv..."
  pip install uv || { echo "Failed to install uv"; exit 1; }
fi

# Remove any existing virtual environment to avoid conflicts
if [ -d ".venv" ]; then
  echo "Removing existing virtual environment..."
  rm -rf .venv
fi

# Create a fresh virtual environment
echo "Creating virtual environment..."
uv venv || { echo "Failed to create virtual environment"; exit 1; }

# Activate the virtual environment
echo "Activating virtual environment..."
. .venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }
echo "Virtual environment activated"

# Install uvicorn and other requirements
echo "Installing uvicorn..."
uv pip install uvicorn || { echo "Failed to install uvicorn"; exit 1; }

echo "Installing requirements..."
uv pip install -r requirements.txt || { echo "Failed to install requirements"; exit 1; }

# Install playwright browsers
echo "Installing playwright browsers..."
playwright install || { echo "Failed to install playwright browsers"; exit 1; }

# Navigate to frontend directory and install npm dependencies
echo "Installing frontend dependencies..."
cd frontend || { echo "Failed to enter frontend directory"; exit 1; }
npm install --legacy-peer-deps || { echo "npm install failed"; exit 1; }

echo "Installation completed successfully!"