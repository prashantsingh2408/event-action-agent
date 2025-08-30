#!/usr/bin/env python3
"""
Complete system test to demonstrate the notification memory system working with the agent.
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import LangChainAgent, notification_memory

def test_complete_system():
    """Test the complete system with memory integration."""
    
    print("🚀 Complete System Test with Memory Integration")
    print("=" * 60)
    
    # Reset memory for clean test
    print("1. Resetting notification memory...")
    notification_memory.reset_memory()
    
    # Create agent
    print("\n2. Creating agent...")
    agent = LangChainAgent()
    
    # Test query that should trigger email notification
    query = "There is any update in tax policy."
    print(f"\n3. Testing query: '{query}'")
    print("-" * 40)
    
    # First run - should find updates and send email
    print("\n   First run (should send email):")
    result1 = agent.run(query)
    print(f"   Result: {result1[:200]}...")  # Show first 200 chars
    
    # Check memory status
    stats1 = notification_memory.get_notification_stats()
    print(f"   Notifications sent: {stats1['total_notifications']}")
    
    # Second run with same query - should NOT send email (duplicate)
    print("\n   Second run (should NOT send email - duplicate):")
    result2 = agent.run(query)
    print(f"   Result: {result2[:200]}...")  # Show first 200 chars
    
    # Check memory status
    stats2 = notification_memory.get_notification_stats()
    print(f"   Notifications sent: {stats2['total_notifications']}")
    
    # Test with different topic
    query2 = "There is any update in budget announcement."
    print(f"\n4. Testing different query: '{query2}'")
    print("-" * 40)
    
    result3 = agent.run(query2)
    print(f"   Result: {result3[:200]}...")  # Show first 200 chars
    
    # Final memory status
    stats3 = notification_memory.get_notification_stats()
    print(f"\n5. Final Memory Status:")
    print(f"   Total notifications: {stats3['total_notifications']}")
    print(f"   Recent notifications (7 days): {stats3['recent_notifications']}")
    print(f"   Notifications by topic: {stats3['notifications_by_topic']}")
    
    # Show recent notifications
    print(f"\n6. Recent Notifications:")
    recent = notification_memory.get_recent_notifications("tax policy", days=7)
    for i, notif in enumerate(recent, 1):
        print(f"   {i}. Topic: {notif['notification_data'].get('topic_searched')}")
        print(f"      Sent at: {notif['sent_at']}")
        print(f"      Updates found: {len(notif['notification_data'].get('relevant_updates', []))}")
        print(f"      Reasoning: {notif['notification_data'].get('reasoning')}")
    
    print("\n✅ Complete system test finished!")

if __name__ == "__main__":
    test_complete_system()
