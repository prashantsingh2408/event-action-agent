#!/usr/bin/env python3
"""
Basic usage example for Event Action Agent.

This example shows how to use the agent programmatically.
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import LangChainAgent, search_web, checkIsMailneedtoSend, notification_memory


def basic_agent_usage():
    """Demonstrate basic agent usage."""
    print("🤖 Event Action Agent - Basic Usage Example")
    print("=" * 50)
    
    # Create agent instance
    agent = LangChainAgent()
    
    # Example 1: Simple query
    print("\n1. Simple Query Example:")
    query = "latest AI developments in 2025"
    print(f"Query: {query}")
    result = agent.run(query)
    print(f"Result: {result[:200]}...")  # Show first 200 chars
    
    # Example 2: Using individual tools
    print("\n2. Individual Tools Example:")
    search_results = search_web.invoke({"query": "tax policy updates", "max_results": 3})
    print(f"Search results: {search_results[:200]}...")
    
    # Example 3: Email notification check
    print("\n3. Email Notification Check:")
    import json
    event_data = {"topic": "budget announcement"}
    email_result = checkIsMailneedtoSend.invoke({"event_data": json.dumps(event_data)})
    print(f"Email check result: {email_result[:200]}...")
    
    # Example 4: Memory system
    print("\n4. Memory System:")
    stats = notification_memory.get_notification_stats()
    print(f"Notification stats: {stats}")


if __name__ == "__main__":
    basic_agent_usage()
