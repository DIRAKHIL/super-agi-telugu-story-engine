#!/usr/bin/env python3
"""
Main entry point for the AI Emotional Engine for Telugu Story Creation.
PRODUCTION-READY REAL AI SYSTEM - 100% open source OPERATIONAL!
"""

import argparse
import sys
import os
import threading
import multiprocessing
from loguru import logger

from src.api.server import start_server
from src.utils.config.config_manager import ConfigManager

# Global variable to store loaded models for access across modules
loaded_models = {}


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="AI Emotional Engine for Telugu Story Creation - PRODUCTION-READY REAL AI SYSTEM"
    )
    parser.add_argument(
        "--init", action="store_true", help="Initialize the system"
    )
    parser.add_argument(
        "--server", action="store_true", help="Start the API server"
    )
    parser.add_argument(
        "--dashboard", action="store_true", help="Start the dashboard"
    )
    parser.add_argument(
        "--all", action="store_true", help="Start both API server and dashboard"
    )
    parser.add_argument(
        "--env", type=str, default="development", 
        help="Environment (development, production, test)"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug mode"
    )
    parser.add_argument(
        "--download-models", action="store_true", help="Download AI models"
    )
    parser.add_argument(
        "--gpu", action="store_true", help="Use GPU for inference"
    )
    
    return parser.parse_args()


def initialize_system(config):
    """Initialize the system components."""
    logger.info("Initializing AI Emotional Engine for Telugu Story Creation...")
    
    # Create necessary directories
    os.makedirs("./models/cache", exist_ok=True)
    os.makedirs("./logs", exist_ok=True)
    os.makedirs("./data", exist_ok=True)
    
    # Initialize database
    from src.utils.database import init_db
    init_db(config)
    
    # Initialize models
    from src.utils.model_loader import load_models
    global loaded_models
    loaded_models = load_models(config)
    
    # Initialize telemetry if enabled
    if config.get("telemetry", {}).get("enabled", False):
        from src.utils.telemetry import init_telemetry
        init_telemetry(config)
    
    # Initialize cache
    if config["cache"]["type"] == "redis":
        try:
            import redis
            redis_client = redis.from_url(config["cache"]["redis_url"])
            redis_client.ping()
            logger.info("Redis cache initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize Redis cache: {e}. Falling back to in-memory cache.")
            config["cache"]["type"] = "memory"
    
    logger.info("System initialization complete.")


def download_models(config):
    """Download AI models for local inference."""
    logger.info("Downloading AI models for local inference...")
    
    from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
    import torch
    
    # Create models directory
    os.makedirs("./models", exist_ok=True)
    
    # Download language model
    language_model = config["models"]["language"]["model_name"]
    logger.info(f"Downloading language model: {language_model}")
    try:
        tokenizer = AutoTokenizer.from_pretrained(language_model, cache_dir="./models/cache")
        model = AutoModel.from_pretrained(language_model, cache_dir="./models/cache")
        logger.info(f"Successfully downloaded language model: {language_model}")
    except Exception as e:
        logger.error(f"Failed to download language model: {e}")
    
    # Download embedding model
    embedding_model = config["models"]["embedding"]["model_name"]
    logger.info(f"Downloading embedding model: {embedding_model}")
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(embedding_model, cache_folder="./models/cache")
        logger.info(f"Successfully downloaded embedding model: {embedding_model}")
    except Exception as e:
        logger.error(f"Failed to download embedding model: {e}")
    
    # Download local LLM if specified
    story_model = config["models"]["story_generation"]["model_name"]
    if story_model.startswith("local:") and not story_model.endswith(".gguf"):
        local_model_path = story_model.replace("local:", "")
        logger.info(f"Downloading local LLM: {local_model_path}")
        try:
            tokenizer = AutoTokenizer.from_pretrained(local_model_path, cache_dir="./models/cache")
            model = AutoModelForCausalLM.from_pretrained(
                local_model_path, 
                cache_dir="./models/cache",
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            logger.info(f"Successfully downloaded local LLM: {local_model_path}")
        except Exception as e:
            logger.error(f"Failed to download local LLM: {e}")
    
    logger.info("Model download complete.")


def start_dashboard(config):
    """Start the dashboard application."""
    logger.info("Starting dashboard...")
    
    from src.dashboard.app import run_dashboard
    dashboard_port = config["dashboard"]["port"]
    debug_mode = config["api"]["debug"]
    
    run_dashboard(port=dashboard_port, debug=debug_mode)


def run_server_and_dashboard(config):
    """Run both the API server and dashboard in separate processes."""
    logger.info("Starting both API server and dashboard...")
    
    # Start API server in a separate process
    server_process = multiprocessing.Process(
        target=start_server,
        args=(config,),
        name="APIServer"
    )
    server_process.start()
    
    # Start dashboard in the main process
    try:
        start_dashboard(config)
    except KeyboardInterrupt:
        logger.info("Shutting down dashboard...")
    finally:
        # Terminate server process when dashboard exits
        if server_process.is_alive():
            server_process.terminate()
            server_process.join()


def main():
    """Main entry point."""
    args = parse_args()
    
    # Set environment variable for GPU usage
    if args.gpu:
        os.environ["USE_GPU"] = "true"
    else:
        os.environ["USE_GPU"] = "false"
    
    # Set environment variable for environment
    os.environ["ENVIRONMENT"] = args.env
    
    # Configure logging
    log_level = "DEBUG" if args.debug else "INFO"
    logger.remove()
    logger.add(sys.stderr, level=log_level)
    logger.add(
        f"./logs/story_engine_{args.env}.log", 
        rotation="50 MB", 
        retention="30 days", 
        level=log_level
    )
    
    # Print banner
    logger.info("=" * 80)
    logger.info("Telugu Story Engine - PRODUCTION-READY REAL AI SYSTEM - 100% open source OPERATIONAL!")
    logger.info("=" * 80)
    
    # Load configuration
    config_manager = ConfigManager()
    config = config_manager.load_config(args.env)
    
    # Override debug setting if specified
    if args.debug:
        config["api"]["debug"] = True
    
    if args.download_models:
        download_models(config)
        return
    
    if args.init:
        initialize_system(config)
        return
    
    # Initialize system in all cases when running services
    initialize_system(config)
    
    if args.all:
        run_server_and_dashboard(config)
        return
    
    if args.server:
        start_server(config)
        return
    
    if args.dashboard:
        start_dashboard(config)
        return
    
    # If no specific command, show help
    logger.info("No command specified. Use --help for available commands.")
    

if __name__ == "__main__":
    # Set multiprocessing start method
    multiprocessing.set_start_method('spawn', force=True)
    main()