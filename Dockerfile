FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04 as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Kolkata

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    curl \
    wget \
    libpq-dev \
    tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p /app/models/cache /app/logs /app/data

# Set up environment variables
ENV PYTHONPATH=/app \
    USE_GPU=true \
    ENVIRONMENT=production

# Expose ports for API and dashboard
EXPOSE 12000 12001

# Create entrypoint script
RUN echo '#!/bin/bash\n\
if [ "$1" = "api" ]; then\n\
    python3 -m src.main --server --env production\n\
elif [ "$1" = "dashboard" ]; then\n\
    python3 -m src.main --dashboard --env production\n\
elif [ "$1" = "all" ]; then\n\
    python3 -m src.main --all --env production\n\
elif [ "$1" = "init" ]; then\n\
    python3 -m src.main --init --env production\n\
elif [ "$1" = "download-models" ]; then\n\
    python3 -m src.main --download-models --env production\n\
else\n\
    exec "$@"\n\
fi' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command
CMD ["all"]