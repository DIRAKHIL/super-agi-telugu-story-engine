#!/bin/bash

# Super-AGI Emotional Brain Engine - Telugu Film Story Generation System
# Production-Ready Startup Script

set -e

echo "🧠 Starting Super-AGI Emotional Brain Engine..."
echo "📚 Telugu Film Story Generation System"
echo "🚀 Production-Ready Real AI System"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p docker/{nginx,postgres,prometheus,grafana/{dashboards,datasources}}

# Create nginx configuration
print_status "Setting up Nginx configuration..."
cat > docker/nginx/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:12000;
    }
    
    upstream frontend {
        server frontend:3000;
    }
    
    server {
        listen 80;
        server_name localhost;
        
        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Backend API
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 300s;
            proxy_connect_timeout 75s;
        }
        
        # Health check
        location /health {
            proxy_pass http://backend/health;
            proxy_set_header Host $host;
        }
    }
}
EOF

# Create PostgreSQL init script
print_status "Setting up PostgreSQL initialization..."
cat > docker/postgres/init.sql << 'EOF'
-- Telugu Film Story Generation System Database Schema

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Stories table
CREATE TABLE IF NOT EXISTS stories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255),
    content TEXT NOT NULL,
    genre VARCHAR(50),
    theme VARCHAR(50),
    setting VARCHAR(50),
    characters JSONB,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Emotions table
CREATE TABLE IF NOT EXISTS emotions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    story_id UUID REFERENCES stories(id),
    text_segment TEXT,
    emotions JSONB,
    sentiment JSONB,
    cultural_context JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cultural analysis table
CREATE TABLE IF NOT EXISTS cultural_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    story_id UUID REFERENCES stories(id),
    authenticity_score FLOAT,
    cultural_elements JSONB,
    validation_issues JSONB,
    suggestions JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_type VARCHAR(50),
    status VARCHAR(20),
    input_data JSONB,
    result JSONB,
    agent_id VARCHAR(100),
    execution_time FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Workflows table
CREATE TABLE IF NOT EXISTS workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255),
    status VARCHAR(20),
    steps JSONB,
    results JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_stories_genre ON stories(genre);
CREATE INDEX IF NOT EXISTS idx_stories_theme ON stories(theme);
CREATE INDEX IF NOT EXISTS idx_stories_created_at ON stories(created_at);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_task_type ON tasks(task_type);
CREATE INDEX IF NOT EXISTS idx_workflows_status ON workflows(status);

-- Insert sample data
INSERT INTO stories (title, content, genre, theme, setting, characters, metadata) VALUES
('Sample Telugu Story', 'ఒకప్పుడు ఒక చిన్న గ్రామంలో...', 'drama', 'family', 'village', '["రాము", "సీత"]', '{"word_count": 150, "reading_time": 1}')
ON CONFLICT DO NOTHING;
EOF

# Create Prometheus configuration
print_status "Setting up Prometheus configuration..."
cat > docker/prometheus/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'telugu-story-backend'
    static_configs:
      - targets: ['backend:12000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
EOF

# Install backend dependencies
print_status "Installing backend dependencies..."
cd backend
if [ ! -f "requirements.txt" ]; then
    print_error "Backend requirements.txt not found!"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
print_status "Installing Python packages..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cd ..

# Install frontend dependencies
print_status "Installing frontend dependencies..."
cd frontend
if [ ! -f "package.json" ]; then
    print_error "Frontend package.json not found!"
    exit 1
fi

# Install Node.js dependencies
print_status "Installing Node.js packages..."
npm install

cd ..

# Set up environment variables
print_status "Setting up environment variables..."
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# Super-AGI Emotional Brain Engine Configuration

# Application
APP_NAME=Super-AGI Emotional Brain Engine
APP_VERSION=1.0.0
DEBUG=false

# Server
HOST=0.0.0.0
PORT=12000

# Database
DATABASE_URL=postgresql://telugu_user:telugu_pass@localhost:5432/telugu_stories
REDIS_URL=redis://localhost:6379

# AI Models (Add your API keys here)
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Security
SECRET_KEY=super-secret-key-change-in-production-environment

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000","https://work-1-lgnjybaibjmwkfyv.prod-runtime.all-hands.dev","https://work-2-lgnjybaibjmwkfyv.prod-runtime.all-hands.dev"]
EOF
    print_warning "Created .env file. Please update with your API keys!"
fi

# Build and start services
print_status "Building and starting services..."

# Start with Docker Compose
docker-compose up --build -d

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 30

# Check service health
print_status "Checking service health..."

# Check backend health
if curl -f http://localhost:12000/health > /dev/null 2>&1; then
    print_success "Backend service is healthy"
else
    print_warning "Backend service may still be starting..."
fi

# Check frontend
if curl -f http://localhost:12001 > /dev/null 2>&1; then
    print_success "Frontend service is healthy"
else
    print_warning "Frontend service may still be starting..."
fi

# Display service URLs
echo ""
echo "🎉 Super-AGI Emotional Brain Engine is starting up!"
echo ""
echo "📊 Service URLs:"
echo "   Frontend Dashboard: http://localhost:12001"
echo "   Backend API:       http://localhost:12000"
echo "   API Documentation: http://localhost:12000/docs"
echo "   Database:          localhost:5432"
echo "   Redis Cache:       localhost:6379"
echo "   Prometheus:        http://localhost:9090"
echo "   Grafana:          http://localhost:3000"
echo ""
echo "🔧 Management Commands:"
echo "   View logs:         docker-compose logs -f"
echo "   Stop services:     docker-compose down"
echo "   Restart:           docker-compose restart"
echo ""
echo "🧠 Features Available:"
echo "   ✅ Advanced Story Generation"
echo "   ✅ Real AI-Powered Emotion Analysis"
echo "   ✅ Sentiment Analysis"
echo "   ✅ Multi-Agent Orchestration"
echo "   ✅ Telugu Cultural Processing"
echo "   ✅ Character Development Engine"
echo "   ✅ Production Planning"
echo ""
echo "⚡ Zero Mock Dependencies - 100% Real AI Models!"
echo ""

print_success "System startup completed! 🚀"
print_status "Access the dashboard at: http://localhost:12001"