#!/usr/bin/env python3
"""
Event Action Agent - Main Entry Point

A clean, modular LangChain-based AI agent with web search capabilities 
using Hugging Face models and intelligent notification memory system.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.cli import CLI


def main():
    """Main application entry point."""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
