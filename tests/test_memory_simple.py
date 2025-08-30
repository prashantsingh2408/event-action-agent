#!/usr/bin/env python3
"""
Simple test script to demonstrate the notification memory system.
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import notification_memory

def test_memory_simple():
    """Test the notification memory system with controlled data."""
    
    print("🧠 Simple Memory System Test")
    print("=" * 50)
    
    # Reset memory for clean test
    print("1. Resetting notification memory...")
    notification_memory.reset_memory()
    
    # Create controlled test data
    topic = "tax policy"
    notification_data1 = {
        "should_send_email": True,
        "reasoning": "Found 3 relevant updates for 'tax policy'",
        "topic_searched": topic,
        "relevant_updates": [
            {"title": "Tax Update 1", "url": "http://example1.com"},
            {"title": "Tax Update 2", "url": "http://example2.com"},
            {"title": "Tax Update 3", "url": "http://example3.com"}
        ]
    }
    
    # Test first call - should NOT be sent before
    print("\n2. Testing if notification was already sent (first time)...")
    is_sent = notification_memory.is_notification_sent(topic, notification_data1)
    print(f"   Already sent: {is_sent}")
    
    # Mark as sent
    print("\n3. Marking notification as sent...")
    key = notification_memory.mark_notification_sent(topic, notification_data1)
    print(f"   Idempotency key: {key}")
    
    # Test second call - should be sent now
    print("\n4. Testing if notification was already sent (second time)...")
    is_sent = notification_memory.is_notification_sent(topic, notification_data1)
    print(f"   Already sent: {is_sent}")
    
    # Test with slightly different data - should NOT be sent
    print("\n5. Testing with slightly different data...")
    notification_data2 = {
        "should_send_email": True,
        "reasoning": "Found 3 relevant updates for 'tax policy'",
        "topic_searched": topic,
        "relevant_updates": [
            {"title": "Tax Update 1", "url": "http://example1.com"},
            {"title": "Tax Update 2", "url": "http://example2.com"},
            {"title": "Tax Update 3", "url": "http://example3.com"}
        ]
    }
    is_sent = notification_memory.is_notification_sent(topic, notification_data2)
    print(f"   Already sent: {is_sent}")
    
    # Test with different topic - should NOT be sent
    print("\n6. Testing with different topic...")
    topic2 = "budget announcement"
    is_sent = notification_memory.is_notification_sent(topic2, notification_data1)
    print(f"   Already sent: {is_sent}")
    
    # Show statistics
    print("\n7. Notification Statistics:")
    stats = notification_memory.get_notification_stats()
    print(f"   Total notifications: {stats['total_notifications']}")
    print(f"   Recent notifications (7 days): {stats['recent_notifications']}")
    print(f"   Notifications by topic: {stats['notifications_by_topic']}")
    
    print("\n✅ Simple memory system test completed!")

if __name__ == "__main__":
    test_memory_simple()
