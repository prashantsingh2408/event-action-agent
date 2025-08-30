#!/usr/bin/env python3
"""
Test to demonstrate the correct workflow and expected output.
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import search_web, checkIsMailneedtoSend, notification_memory

def test_correct_workflow():
    """Test the correct workflow manually."""
    print("🧪 Testing Correct Workflow")
    print("=" * 50)
    
    # Reset memory
    notification_memory.reset_memory()
    
    # Step 1: Search for updates
    print("1. Searching for climate policy updates...")
    search_results = search_web.invoke({"query": "climate policy updates", "max_results": 5})
    print(f"Search results: {search_results[:200]}...")
    
    # Step 2: Check if email should be sent
    print("\n2. Checking if email should be sent...")
    event_data = {"topic": "climate policy"}
    email_result = checkIsMailneedtoSend.invoke({"event_data": json.dumps(event_data)})
    email_data = json.loads(email_result)
    
    print(f"Email decision: {email_data.get('should_send_email')}")
    print(f"Reasoning: {email_data.get('reasoning')}")
    
    # Step 3: Provide comprehensive response
    print("\n3. Comprehensive Response:")
    print("=" * 50)
    
    print("**Climate Policy Updates Analysis**")
    print()
    
    # Parse search results
    search_data = json.loads(search_results)
    print("**Search Results Summary:**")
    for i, result in enumerate(search_data, 1):
        print(f"{i}. {result.get('title', 'No title')}")
        print(f"   URL: {result.get('url', 'No URL')}")
        print(f"   Summary: {result.get('snippet', 'No snippet')[:100]}...")
        print()
    
    print("**Email Decision:**")
    print(f"Should send email: {email_data.get('should_send_email')}")
    print(f"Reasoning: {email_data.get('reasoning')}")
    print(f"Topic searched: {email_data.get('topic_searched')}")
    print(f"Relevant updates found: {len(email_data.get('relevant_updates', []))}")
    
    print("\n**Key Updates Found:**")
    relevant_updates = email_data.get('relevant_updates', [])
    for i, update in enumerate(relevant_updates, 1):
        print(f"{i}. {update.get('title', 'No title')}")
        print(f"   URL: {update.get('url', 'No URL')}")
    
    print("\n✅ This is what the agent should output!")

if __name__ == "__main__":
    test_correct_workflow()
