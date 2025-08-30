#!/usr/bin/env python3
"""
Test script to verify the checkIsMailneedtoSend function works correctly.
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import checkIsMailneedtoSend

def test_email_check():
    """Test the checkIsMailneedtoSend function."""
    event_data = {"topic": "tax policy"}
    print("Testing checkIsMailneedtoSend with tax policy...")
    result = checkIsMailneedtoSend(json.dumps(event_data))
    print("Result:", result)
    print()
    event_data = {"topic": "budget announcement"}
    print("Testing checkIsMailneedtoSend with budget announcement...")
    result = checkIsMailneedtoSend(json.dumps(event_data))
    print("Result:", result)
    print()

if __name__ == "__main__":
    test_email_check()
