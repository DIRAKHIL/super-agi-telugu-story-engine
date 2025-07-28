#!/usr/bin/env python3
"""
Main entry point for the AI Emotional Engine for Telugu Story Creation.
"""

import argparse
import sys
from loguru import logger

from src.api.server import start_server
from src.utils.config.config_manager import ConfigManager


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="AI Emotional Engine for Telugu Story Creation"
    )
    parser.add_argument(
        "--init", action="store_true", help="Initialize the system"
    )
    parser.add_argument(
        "--server", action="store_true", help="Start the API server"
    )
    parser.add_argument(
        "--env", type=str, default="development", 
        help="Environment (development, production, test)"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug mode"
    )
    
    return parser.parse_args()


def initialize_system(config):
    """Initialize the system components."""
    logger.info("Initializing AI Emotional Engine for Telugu Story Creation...")
    
    # Initialize database
    from src.utils.database import init_db
    init_db(config)
    
    # Initialize models
    from src.utils.model_loader import load_models
    load_models(config)
    
    logger.info("System initialization complete.")


def main():
    """Main entry point."""
    args = parse_args()
    
    # Configure logging
    log_level = "DEBUG" if args.debug else "INFO"
    logger.remove()
    logger.add(sys.stderr, level=log_level)
    
    # Load configuration
    config_manager = ConfigManager()
    config = config_manager.load_config(args.env)
    
    if args.init:
        initialize_system(config)
        return
    
    if args.server:
        start_server(config)
        return
    
    # If no specific command, show help
    logger.info("No command specified. Use --help for available commands.")
    

if __name__ == "__main__":
    main()