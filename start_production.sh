#!/bin/bash
# Production startup script for Telugu Story Engine
# PRODUCTION-READY REAL AI SYSTEM - 100% open source OPERATIONAL!

# Set environment variables
export ENVIRONMENT=production
export USE_GPU=true
export LOG_LEVEL=INFO

# Create necessary directories
mkdir -p ./models/cache ./logs ./data

# Check if models are downloaded
if [ ! -f "./models/llama-3-70b-telugu-instruct.gguf" ]; then
    echo "Models not found. Downloading models..."
    python -m src.main --download-models --env production
fi

# Initialize the system if needed
if [ ! -f "./initialized.flag" ]; then
    echo "Initializing system..."
    python -m src.main --init --env production
    touch ./initialized.flag
fi

# Start the system with both API server and dashboard
echo "Starting Telugu Story Engine - PRODUCTION-READY REAL AI SYSTEM..."
echo "=============================================================="
python -m src.main --all --env production