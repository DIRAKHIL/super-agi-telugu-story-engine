#!/usr/bin/env python3
"""
Main Entry Point for Telugu Story Engine
Production-ready AI system launcher - NO MOCKS, NO FALLBACKS
"""

import asyncio
import logging
import sys
import os
from pathlib import Path
import click
import uvicorn
from multiprocessing import Process

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.config import get_config, get_development_config, get_production_config
from src.core.model_manager import initialize_models
from src.api.main import app
from src.dashboard.main import main as dashboard_main

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/telugu_story_engine.log')
    ]
)
logger = logging.getLogger(__name__)

@click.group()
def cli():
    """Telugu Story Engine - Production AI System for Telugu Story Generation"""
    pass

@cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=12000, help='Port to bind to')
@click.option('--workers', default=1, help='Number of worker processes')
@click.option('--reload', is_flag=True, help='Enable auto-reload for development')
@click.option('--env', default='production', type=click.Choice(['development', 'production', 'testing']))
def serve(host, port, workers, reload, env):
    """Start the API server"""
    logger.info(f"Starting Telugu Story Engine API server in {env} mode...")
    
    # Set configuration based on environment
    if env == 'development':
        config = get_development_config()
    elif env == 'testing':
        from src.core.config import get_testing_config
        config = get_testing_config()
    else:
        config = get_production_config()
    
    # Update configuration
    config.api.host = host
    config.api.port = port
    config.api.reload = reload
    config.environment = env
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Run server
    uvicorn.run(
        "src.api.main:app",
        host=host,
        port=port,
        workers=workers if not reload else 1,
        reload=reload,
        log_level="info",
        access_log=True
    )

@cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=12001, help='Port to bind to')
def dashboard(host, port):
    """Start the dashboard"""
    logger.info("Starting Telugu Story Engine Dashboard...")
    
    # Set Streamlit configuration
    os.environ['STREAMLIT_SERVER_PORT'] = str(port)
    os.environ['STREAMLIT_SERVER_ADDRESS'] = host
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    # Run dashboard
    dashboard_main()

@cli.command()
@click.option('--api-host', default='0.0.0.0', help='API host')
@click.option('--api-port', default=12000, help='API port')
@click.option('--dashboard-host', default='0.0.0.0', help='Dashboard host')
@click.option('--dashboard-port', default=12001, help='Dashboard port')
@click.option('--env', default='production', type=click.Choice(['development', 'production']))
def run(api_host, api_port, dashboard_host, dashboard_port, env):
    """Run both API and Dashboard"""
    logger.info("Starting Telugu Story Engine (API + Dashboard)...")
    
    def start_api():
        """Start API server"""
        uvicorn.run(
            "src.api.main:app",
            host=api_host,
            port=api_port,
            workers=1 if env == 'development' else 4,
            reload=env == 'development',
            log_level="info"
        )
    
    def start_dashboard():
        """Start dashboard"""
        os.environ['STREAMLIT_SERVER_PORT'] = str(dashboard_port)
        os.environ['STREAMLIT_SERVER_ADDRESS'] = dashboard_host
        os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
        os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
        
        import streamlit.web.cli as stcli
        sys.argv = ["streamlit", "run", "src/dashboard/main.py"]
        stcli.main()
    
    # Start both processes
    api_process = Process(target=start_api)
    dashboard_process = Process(target=start_dashboard)
    
    try:
        api_process.start()
        dashboard_process.start()
        
        logger.info(f"API running on http://{api_host}:{api_port}")
        logger.info(f"Dashboard running on http://{dashboard_host}:{dashboard_port}")
        logger.info("Press Ctrl+C to stop both services")
        
        # Wait for processes
        api_process.join()
        dashboard_process.join()
        
    except KeyboardInterrupt:
        logger.info("Shutting down services...")
        api_process.terminate()
        dashboard_process.terminate()
        api_process.join()
        dashboard_process.join()

@cli.command()
async def init():
    """Initialize the system (download models, setup database, etc.)"""
    logger.info("Initializing Telugu Story Engine...")
    
    # Create necessary directories
    directories = ['data/models', 'data/cache', 'data/stories', 'logs', 'config']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Created directory: {directory}")
    
    # Initialize models
    logger.info("Initializing AI models...")
    try:
        await initialize_models()
        logger.info("Models initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize models: {e}")
        return
    
    # Create default configuration
    config_path = Path("config/production.env")
    if not config_path.exists():
        default_config = """
# Telugu Story Engine Configuration
ENVIRONMENT=production
DEBUG=false

# API Configuration
API_HOST=0.0.0.0
API_PORT=12000
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/telugu_story_engine
REDIS_URL=redis://localhost:6379/0

# Model Configuration
MODEL_CACHE_DIR=data/cache
MODEL_DATA_DIR=data/models

# Dashboard Configuration
DASHBOARD_HOST=0.0.0.0
DASHBOARD_PORT=12001
"""
        with open(config_path, 'w') as f:
            f.write(default_config)
        logger.info(f"Created default configuration: {config_path}")
    
    logger.info("Initialization complete!")

@cli.command()
@click.argument('prompt')
@click.option('--story-type', default='drama', help='Type of story')
@click.option('--length', default=2000, help='Target word count')
@click.option('--cultural-context', default='contemporary_telugu', help='Cultural context')
def generate(prompt, story_type, length, cultural_context):
    """Generate a story from command line"""
    logger.info("Generating story...")
    
    # This would call the API or directly use the story generation system
    # For now, just show the parameters
    click.echo(f"Generating story with:")
    click.echo(f"  Prompt: {prompt}")
    click.echo(f"  Type: {story_type}")
    click.echo(f"  Length: {length}")
    click.echo(f"  Cultural Context: {cultural_context}")
    
    # TODO: Implement direct story generation
    click.echo("Story generation from CLI not yet implemented. Use the API or dashboard.")

@cli.command()
def status():
    """Check system status"""
    logger.info("Checking system status...")
    
    # Check if models are available
    try:
        from src.core.model_manager import get_model_manager
        model_manager = get_model_manager()
        model_info = model_manager.get_model_info()
        
        click.echo("System Status:")
        click.echo(f"  Models loaded: {len([m for m in model_info.values() if m.loaded])}/{len(model_info)}")
        
        for name, info in model_info.items():
            status = "✓" if info.loaded else "✗"
            click.echo(f"    {status} {name}: {info.model_type}")
        
    except Exception as e:
        click.echo(f"Error checking status: {e}")

@cli.command()
def test():
    """Run system tests"""
    logger.info("Running system tests...")
    
    import subprocess
    try:
        result = subprocess.run(['python', '-m', 'pytest', 'src/tests/', '-v'], 
                              capture_output=True, text=True)
        click.echo(result.stdout)
        if result.stderr:
            click.echo(result.stderr)
        
        if result.returncode == 0:
            click.echo("All tests passed!")
        else:
            click.echo("Some tests failed!")
            sys.exit(1)
            
    except FileNotFoundError:
        click.echo("pytest not found. Install with: pip install pytest")
        sys.exit(1)

@cli.command()
def docker():
    """Build and run Docker container"""
    logger.info("Building Docker container...")
    
    import subprocess
    
    # Build Docker image
    try:
        subprocess.run(['docker', 'build', '-t', 'telugu-story-engine', '.'], check=True)
        click.echo("Docker image built successfully!")
        
        # Run container
        click.echo("Starting container...")
        subprocess.run([
            'docker', 'run', '-p', '12000:12000', '-p', '12001:12001',
            '--name', 'telugu-story-engine-container',
            'telugu-story-engine'
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        click.echo(f"Docker command failed: {e}")
        sys.exit(1)
    except FileNotFoundError:
        click.echo("Docker not found. Please install Docker.")
        sys.exit(1)

if __name__ == '__main__':
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    # Run CLI
    cli()