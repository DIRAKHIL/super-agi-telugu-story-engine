#!/bin/bash
# Production dashboard startup script for Telugu Story Engine
# PRODUCTION-READY REAL AI SYSTEM - 100% open source OPERATIONAL!

# Set environment variables
export ENVIRONMENT=production
export USE_GPU=true
export LOG_LEVEL=INFO
export PORT=12001

# Create necessary directories
mkdir -p ./models/cache ./logs ./data

# Change to script directory
cd "$(dirname "$0")"

# Start the dashboard
echo "Starting Telugu Story Engine Dashboard - PRODUCTION-READY REAL AI SYSTEM..."
echo "=============================================================="
echo "Dashboard running on port: $PORT"
python -m src.main --dashboard --env production