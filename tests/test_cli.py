#!/usr/bin/env python3
"""
Tests for CLI functionality.
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cli import CLI
from src.agent import notification_memory


class TestCLI(unittest.TestCase):
    """Test CLI functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Reset memory for clean tests
        notification_memory.reset_memory()
        self.cli = CLI()
    
    def test_cli_initialization(self):
        """Test CLI initialization."""
        self.assertIsNotNone(self.cli)
        self.assertIsNotNone(self.cli.examples)
        self.assertGreater(len(self.cli.examples), 0)
    
    def test_show_status(self):
        """Test status display functionality."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.cli.show_status()
            output = fake_output.getvalue()
            
            # Check that status information is displayed
            self.assertIn("Hugging Face Provider Status", output)
            self.assertIn("HUGGINGFACE", output)
    
    def test_show_memory_status(self):
        """Test memory status display."""
        # Add some test notifications
        notification_data = {
            "should_send_email": True,
            "reasoning": "Test",
            "topic_searched": "test topic",
            "relevant_updates": [{"title": "Test", "url": "http://test.com"}]
        }
        notification_memory.mark_notification_sent("test topic", notification_data)
        
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.cli.show_memory_status()
            output = fake_output.getvalue()
            
            # Check that memory information is displayed
            self.assertIn("Notification Memory Status", output)
            self.assertIn("Total notifications", output)
    
    def test_show_examples(self):
        """Test examples display."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.cli.show_examples()
            output = fake_output.getvalue()
            
            # Check that examples are displayed
            self.assertIn("Available example queries", output)
            self.assertIn("latest AI developments", output)
    
    def test_get_user_query_with_args(self):
        """Test getting user query from command line arguments."""
        test_query = "test query from args"
        
        with patch('sys.argv', ['main.py', test_query]):
            query = self.cli.get_user_query()
            self.assertEqual(query, test_query)
    
    @patch('builtins.input', return_value='2')
    def test_get_user_query_interactive(self, mock_input):
        """Test getting user query interactively."""
        with patch('sys.argv', ['main.py']):
            query = self.cli.get_user_query()
            self.assertEqual(query, self.cli.examples[1])  # Second example
    
    @patch('builtins.input', return_value='')
    def test_get_user_query_default(self, mock_input):
        """Test getting user query with default selection."""
        with patch('sys.argv', ['main.py']):
            query = self.cli.get_user_query()
            self.assertEqual(query, self.cli.examples[0])  # First example
    
    def test_reset_memory(self):
        """Test memory reset functionality."""
        # Add some test notifications
        notification_data = {
            "should_send_email": True,
            "reasoning": "Test",
            "topic_searched": "test topic",
            "relevant_updates": [{"title": "Test", "url": "http://test.com"}]
        }
        notification_memory.mark_notification_sent("test topic", notification_data)
        
        # Verify notification was added
        stats_before = notification_memory.get_notification_stats()
        self.assertEqual(stats_before["total_notifications"], 1)
        
        # Reset memory
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.cli.reset_memory()
            output = fake_output.getvalue()
            
            # Check reset message
            self.assertIn("Resetting notification memory", output)
            self.assertIn("Notification memory has been reset", output)
        
        # Verify memory was reset
        stats_after = notification_memory.get_notification_stats()
        self.assertEqual(stats_after["total_notifications"], 0)
    
    def test_show_recent_notifications(self):
        """Test recent notifications display."""
        # Add some test notifications
        topics = ["topic1", "topic2"]
        for topic in topics:
            notification_data = {
                "should_send_email": True,
                "reasoning": f"Test for {topic}",
                "topic_searched": topic,
                "relevant_updates": [{"title": f"Update for {topic}", "url": f"http://{topic}.com"}]
            }
            notification_memory.mark_notification_sent(topic, notification_data)
        
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.cli.show_recent_notifications()
            output = fake_output.getvalue()
            
            # Check that notifications are displayed
            self.assertIn("Recent notifications", output)
            self.assertIn("topic1", output)
            self.assertIn("topic2", output)
    
    def test_show_recent_notifications_for_topic(self):
        """Test recent notifications display for specific topic."""
        # Add test notifications
        notification_data = {
            "should_send_email": True,
            "reasoning": "Test",
            "topic_searched": "specific topic",
            "relevant_updates": [{"title": "Test Update", "url": "http://test.com"}]
        }
        notification_memory.mark_notification_sent("specific topic", notification_data)
        
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.cli.show_recent_notifications("specific topic")
            output = fake_output.getvalue()
            
            # Check that specific topic notifications are displayed
            self.assertIn("Recent notifications for 'specific topic'", output)
            self.assertIn("specific topic", output)
    
    def test_show_recent_notifications_empty(self):
        """Test recent notifications display when empty."""
        # Reset memory to ensure it's empty
        notification_memory.reset_memory()
        
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.cli.show_recent_notifications()
            output = fake_output.getvalue()
            
            # Check that empty message is displayed
            self.assertIn("Recent notifications", output)
            self.assertIn("No recent notifications found", output)
    
    @patch('src.cli.cli.LangChainAgent')
    def test_run_agent(self, mock_agent_class):
        """Test agent execution."""
        # Mock agent
        mock_agent = MagicMock()
        mock_agent.run.return_value = "Test agent response"
        mock_agent_class.return_value = mock_agent
        
        test_query = "test query"
        
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.cli.run_agent(test_query)
            output = fake_output.getvalue()
            
            # Check that agent was called and output displayed
            mock_agent.run.assert_called_once_with(test_query)
            self.assertIn("Query: test query", output)
            self.assertIn("AI Agent: Processing your request", output)
            self.assertIn("Test agent response", output)


if __name__ == "__main__":
    unittest.main()
