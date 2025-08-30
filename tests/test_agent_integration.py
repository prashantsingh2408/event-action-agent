#!/usr/bin/env python3
"""
Integration tests for the LangChain agent with all tools.
"""

import sys
import os
import json
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import LangChainAgent, search_web, checkIsMailneedtoSend, notification_memory


class TestAgentIntegration(unittest.TestCase):
    """Test agent integration with tools and memory."""
    
    def setUp(self):
        """Set up test environment."""
        # Reset memory for clean tests
        notification_memory.reset_memory()
        
        # Mock the LLM to avoid API calls during testing
        with patch('src.agent.agent.ChatOpenAI'):
            self.agent = LangChainAgent()
    
    def test_agent_initialization(self):
        """Test that agent initializes correctly."""
        self.assertIsNotNone(self.agent)
        self.assertIsNotNone(self.agent.tools)
        self.assertEqual(len(self.agent.tools), 2)
        self.assertIn(search_web, self.agent.tools)
        self.assertIn(checkIsMailneedtoSend, self.agent.tools)
    
    def test_tools_availability(self):
        """Test that all required tools are available."""
        tool_names = [tool.name for tool in self.agent.tools]
        self.assertIn('search_web', tool_names)
        self.assertIn('checkIsMailneedtoSend', tool_names)
    
    @patch('src.agent.tools.DDGS')
    def test_search_web_tool(self, mock_ddgs):
        """Test search_web tool functionality."""
        # Mock search results
        mock_results = [
            {
                "title": "Test Result 1",
                "href": "http://example1.com",
                "body": "This is a test result"
            },
            {
                "title": "Test Result 2",
                "href": "http://example2.com",
                "body": "Another test result"
            }
        ]
        
        mock_ddgs_instance = MagicMock()
        mock_ddgs_instance.text.return_value = mock_results
        mock_ddgs.return_value.__enter__.return_value = mock_ddgs_instance
        
        # Test the tool
        result = search_web.invoke({"query": "test query", "max_results": 2})
        result_data = json.loads(result)
        
        self.assertEqual(len(result_data), 2)
        self.assertEqual(result_data[0]["title"], "Test Result 1")
        self.assertEqual(result_data[1]["title"], "Test Result 2")
    
    @patch('src.agent.tools.DDGS')
    def test_checkIsMailneedtoSend_tool(self, mock_ddgs):
        """Test checkIsMailneedtoSend tool functionality."""
        # Mock search results
        mock_results = [
            {
                "title": "Latest Tax Update 2025",
                "href": "http://example.com/tax-update",
                "body": "New tax policy announced today"
            }
        ]
        
        mock_ddgs_instance = MagicMock()
        mock_ddgs_instance.text.return_value = mock_results
        mock_ddgs.return_value.__enter__.return_value = mock_ddgs_instance
        
        # Test the tool
        event_data = {"topic": "tax policy"}
        result = checkIsMailneedtoSend.invoke({"event_data": json.dumps(event_data)})
        result_data = json.loads(result)
        
        self.assertIn("should_send_email", result_data)
        self.assertIn("reasoning", result_data)
        self.assertIn("topic_searched", result_data)
        self.assertEqual(result_data["topic_searched"], "tax policy")
    
    def test_memory_integration(self):
        """Test that memory system integrates with tools."""
        # Create test notification data
        topic = "test topic"
        notification_data = {
            "should_send_email": True,
            "reasoning": "Test notification",
            "topic_searched": topic,
            "relevant_updates": [
                {"title": "Test Update", "url": "http://test.com"}
            ]
        }
        
        # Test that notification is not sent initially
        self.assertFalse(notification_memory.is_notification_sent(topic, notification_data))
        
        # Mark as sent
        key = notification_memory.mark_notification_sent(topic, notification_data)
        self.assertIsNotNone(key)
        
        # Test that notification is now marked as sent
        self.assertTrue(notification_memory.is_notification_sent(topic, notification_data))
    
    def test_duplicate_prevention(self):
        """Test that duplicate notifications are prevented."""
        topic = "duplicate test"
        notification_data = {
            "should_send_email": True,
            "reasoning": "Duplicate test",
            "topic_searched": topic,
            "relevant_updates": [
                {"title": "Same Update", "url": "http://same.com"}
            ]
        }
        
        # First call - should not be sent
        self.assertFalse(notification_memory.is_notification_sent(topic, notification_data))
        
        # Mark as sent
        notification_memory.mark_notification_sent(topic, notification_data)
        
        # Second call - should be marked as sent
        self.assertTrue(notification_memory.is_notification_sent(topic, notification_data))
    
    def test_different_topics_dont_conflict(self):
        """Test that different topics don't conflict in memory."""
        topic1 = "topic 1"
        topic2 = "topic 2"
        notification_data = {
            "should_send_email": True,
            "reasoning": "Test",
            "relevant_updates": [
                {"title": "Update", "url": "http://test.com"}
            ]
        }
        
        # Mark topic1 as sent
        notification_memory.mark_notification_sent(topic1, notification_data)
        
        # Topic1 should be sent
        self.assertTrue(notification_memory.is_notification_sent(topic1, notification_data))
        
        # Topic2 should not be sent (different topic)
        self.assertFalse(notification_memory.is_notification_sent(topic2, notification_data))
    
    def test_notification_statistics(self):
        """Test notification statistics functionality."""
        # Reset memory
        notification_memory.reset_memory()
        
        # Get initial stats
        initial_stats = notification_memory.get_notification_stats()
        self.assertEqual(initial_stats["total_notifications"], 0)
        
        # Add some notifications
        topics = ["topic1", "topic2", "topic3"]
        for topic in topics:
            notification_data = {
                "should_send_email": True,
                "reasoning": f"Test for {topic}",
                "topic_searched": topic,
                "relevant_updates": [
                    {"title": f"Update for {topic}", "url": f"http://{topic}.com"}
                ]
            }
            notification_memory.mark_notification_sent(topic, notification_data)
        
        # Check final stats
        final_stats = notification_memory.get_notification_stats()
        self.assertEqual(final_stats["total_notifications"], 3)
        self.assertEqual(len(final_stats["notifications_by_topic"]), 3)
        for topic in topics:
            self.assertIn(topic, final_stats["notifications_by_topic"])


if __name__ == "__main__":
    unittest.main()
