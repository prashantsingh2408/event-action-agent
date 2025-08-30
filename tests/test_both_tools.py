#!/usr/bin/env python3
"""
Test script to verify both tools work correctly when called directly.
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import search_web, checkIsMailneedtoSend

def test_both_tools():
    """Test both tools directly."""
    print("Testing both tools directly...")
    print("=" * 50)
    search_result = search_web.invoke({"query": "tax policy update 2025", "max_results": 3})
    print(f"Search result: {search_result}")
    print()
    print("2. Testing checkIsMailneedtoSend...")
    event_data = {"topic": "tax policy"}
    email_result = checkIsMailneedtoSend.invoke({"event_data": json.dumps(event_data)})
    print(f"Email check result: {email_result}")
    print()
    print("3. Parsed results:")
    try:
        email_data = json.loads(email_result)
        print(f"Should send email: {email_data.get('should_send_email')}")
        print(f"Reasoning: {email_data.get('reasoning')}")
        print(f"Topic searched: {email_data.get('topic_searched')}")
        print(f"Relevant updates found: {len(email_data.get('relevant_updates', []))}")
    except Exception as e:
        print(f"Error parsing result: {e}")

if __name__ == "__main__":
    test_both_tools()
