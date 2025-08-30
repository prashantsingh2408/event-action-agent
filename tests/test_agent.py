#!/usr/bin/env python3
"""
Test script to verify the agent can use both tools correctly.
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import LangChainAgent

def test_agent():
    """Test the agent with both tools."""
    agent = LangChainAgent()
    query = "There is any update in tax policy."
    print(f"Testing query: {query}")
    print("=" * 50)
    result = agent.run(query)
    print(f"Agent result: {result}")
    print("=" * 50)

if __name__ == "__main__":
    test_agent()
