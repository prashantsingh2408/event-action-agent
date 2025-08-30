#!/usr/bin/env python3
"""
Test script to verify the notification memory system prevents duplicate emails.
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import checkIsMailneedtoSend, notification_memory

def test_memory_system():
    """Test the notification memory system."""
    
    print("🧠 Testing Notification Memory System")
    print("=" * 50)
    
    # Reset memory for clean test
    print("1. Resetting notification memory...")
    notification_memory.reset_memory()
    
    # Test first call - should send email
    print("\n2. First call - should send email...")
    event_data = {"topic": "tax policy"}
    result1 = checkIsMailneedtoSend.invoke({"event_data": json.dumps(event_data)})
    result1_data = json.loads(result1)
    
    print(f"   Should send email: {result1_data.get('should_send_email')}")
    print(f"   Reasoning: {result1_data.get('reasoning')}")
    print(f"   Relevant updates found: {len(result1_data.get('relevant_updates', []))}")
    
    # Test second call with same data - should NOT send email (duplicate)
    print("\n3. Second call with same data - should NOT send email (duplicate)...")
    result2 = checkIsMailneedtoSend.invoke({"event_data": json.dumps(event_data)})
    result2_data = json.loads(result2)
    
    print(f"   Should send email: {result2_data.get('should_send_email')}")
    print(f"   Reasoning: {result2_data.get('reasoning')}")
    print(f"   Relevant updates found: {len(result2_data.get('relevant_updates', []))}")
    
    # Test with different topic - should send email
    print("\n4. Test with different topic - should send email...")
    event_data2 = {"topic": "budget announcement"}
    result3 = checkIsMailneedtoSend.invoke({"event_data": json.dumps(event_data2)})
    result3_data = json.loads(result3)
    
    print(f"   Should send email: {result3_data.get('should_send_email')}")
    print(f"   Reasoning: {result3_data.get('reasoning')}")
    print(f"   Relevant updates found: {len(result3_data.get('relevant_updates', []))}")
    
    # Show notification statistics
    print("\n5. Notification Statistics:")
    stats = notification_memory.get_notification_stats()
    print(f"   Total notifications: {stats['total_notifications']}")
    print(f"   Recent notifications (7 days): {stats['recent_notifications']}")
    print(f"   Notifications by topic: {stats['notifications_by_topic']}")
    
    # Show recent notifications for tax policy
    print("\n6. Recent notifications for 'tax policy':")
    recent = notification_memory.get_recent_notifications("tax policy", days=7)
    print(f"   Found {len(recent)} recent notifications")
    for i, notif in enumerate(recent, 1):
        print(f"   {i}. Sent at: {notif['sent_at']}")
        print(f"      Recipient: {notif['recipient']}")
        print(f"      Updates found: {len(notif['notification_data'].get('relevant_updates', []))}")
    
    print("\n✅ Memory system test completed!")

if __name__ == "__main__":
    test_memory_system()
