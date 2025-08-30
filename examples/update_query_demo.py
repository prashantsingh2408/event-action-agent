#!/usr/bin/env python3
"""
Demonstration of the correct workflow for update queries with email decision.
This shows what the agent should be doing.
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import search_web, checkIsMailneedtoSend, notification_memory

def demonstrate_update_query_workflow():
    """Demonstrate the correct workflow for update queries."""
    print("🎯 Update Query Workflow Demonstration")
    print("=" * 60)
    
    # Reset memory for clean demo
    notification_memory.reset_memory()
    
    # Example query
    query = "There is any update in budget policy"
    print(f"Query: {query}")
    print()
    
    # Step 1: Search for updates
    print("1. 🔍 Searching for updates...")
    search_results = search_web.invoke({"query": "budget policy updates", "max_results": 5})
    search_data = json.loads(search_results)
    
    print(f"   Found {len(search_data)} search results")
    for i, result in enumerate(search_data, 1):
        print(f"   {i}. {result.get('title', 'No title')}")
    print()
    
    # Step 2: Check if email should be sent
    print("2. 📧 Checking if email should be sent...")
    event_data = {"topic": "budget policy"}
    email_result = checkIsMailneedtoSend.invoke({"event_data": json.dumps(event_data)})
    email_data = json.loads(email_result)
    
    print(f"   Should send email: {email_data.get('should_send_email')}")
    print(f"   Reasoning: {email_data.get('reasoning')}")
    print(f"   Topic searched: {email_data.get('topic_searched')}")
    print(f"   Relevant updates found: {len(email_data.get('relevant_updates', []))}")
    print()
    
    # Step 3: Provide comprehensive response
    print("3. 📊 Comprehensive Response:")
    print("=" * 60)
    
    print("**Budget Policy Updates Analysis**")
    print()
    
    # Search results summary
    print("**Search Results Summary:**")
    for i, result in enumerate(search_data, 1):
        print(f"{i}. {result.get('title', 'No title')}")
        print(f"   URL: {result.get('url', 'No URL')}")
        print(f"   Summary: {result.get('snippet', 'No snippet')[:100]}...")
        print()
    
    # Email decision
    print("**📧 Email Notification Decision:**")
    print(f"- Should send email: {email_data.get('should_send_email')}")
    print(f"- Reasoning: {email_data.get('reasoning')}")
    print(f"- Topic searched: {email_data.get('topic_searched')}")
    print(f"- Relevant updates found: {len(email_data.get('relevant_updates', []))}")
    print()
    
    # Key updates found
    print("**Key Updates Found:**")
    relevant_updates = email_data.get('relevant_updates', [])
    for i, update in enumerate(relevant_updates, 1):
        print(f"{i}. {update.get('title', 'No title')}")
        print(f"   URL: {update.get('url', 'No URL')}")
    print()
    
    # Memory status
    print("**🧠 Memory Status:**")
    stats = notification_memory.get_notification_stats()
    print(f"- Total notifications: {stats['total_notifications']}")
    print(f"- Recent notifications: {stats['recent_notifications']}")
    print(f"- Notifications by topic: {stats['notifications_by_topic']}")
    print()
    
    print("✅ This is the complete workflow the agent should follow!")
    print("✅ The agent should show BOTH search results AND email decision!")
    print("✅ The email decision shows whether to send notification or not!")

if __name__ == "__main__":
    demonstrate_update_query_workflow()
