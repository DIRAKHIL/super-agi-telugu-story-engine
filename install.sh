#!/bin/bash
# Installation script for Telugu Story Engine
# PRODUCTION-READY REAL AI SYSTEM - 100% open source OPERATIONAL!

echo "Installing Telugu Story Engine - PRODUCTION-READY REAL AI SYSTEM..."
echo "=============================================================="

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p ./models/cache ./logs ./data

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file from .env.example. Please update it with your settings."
fi

# Download models
echo "Downloading AI models..."
python -m src.main --download-models --env production

# Initialize the system
echo "Initializing the system..."
python -m src.main --init --env production

echo "=============================================================="
echo "Installation complete!"
echo "To start the system, run:"
echo "  ./start_production.sh    # Start both API server and dashboard"
echo "  ./start_server.sh        # Start API server only"
echo "  ./start_dashboard.sh     # Start dashboard only"
echo "=============================================================="