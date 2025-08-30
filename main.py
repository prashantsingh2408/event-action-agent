#!/usr/bin/env python3
"""
Event Action Agent - A modular LangChain-based AI agent with web search capabilities.

This application provides an AI agent that can search the web for current information
and provide comprehensive analysis using Hugging Face models.

Usage:
    python main.py                    # Interactive mode with examples
    python main.py "your query"       # Direct query mode
    python main.py --status           # Show configuration status
    python main.py -s                 # Show configuration status (short)
"""

from cli import CLI


def main():
    """Main entry point for the application."""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
