#!/usr/bin/env python3
"""
Test configuration and utilities for Event Action Agent tests.
"""

import os
import tempfile
import sqlite3
from unittest.mock import patch


class TestConfig:
    """Test configuration class."""
    
    # Test database path
    TEST_DB_PATH = "test_notification_memory.db"
    
    # Test data
    SAMPLE_NOTIFICATION_DATA = {
        "should_send_email": True,
        "reasoning": "Test notification",
        "topic_searched": "test topic",
        "relevant_updates": [
            {"title": "Test Update 1", "url": "http://test1.com"},
            {"title": "Test Update 2", "url": "http://test2.com"}
        ]
    }
    
    SAMPLE_SEARCH_RESULTS = [
        {
            "title": "Test Search Result 1",
            "url": "http://search1.com",
            "snippet": "This is a test search result"
        },
        {
            "title": "Test Search Result 2", 
            "url": "http://search2.com",
            "snippet": "Another test search result"
        }
    ]
    
    @classmethod
    def create_temp_db(cls):
        """Create a temporary database for testing."""
        return tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    
    @classmethod
    def cleanup_temp_db(cls, db_path):
        """Clean up temporary database."""
        try:
            os.unlink(db_path)
        except OSError:
            pass
    
    @classmethod
    def setup_test_environment(cls):
        """Set up test environment."""
        # Create test database
        temp_db = cls.create_temp_db()
        temp_db.close()
        
        return temp_db.name
    
    @classmethod
    def teardown_test_environment(cls, db_path):
        """Tear down test environment."""
        cls.cleanup_temp_db(db_path)


class MockDDGS:
    """Mock DDGS class for testing."""
    
    def __init__(self, results=None):
        self.results = results or TestConfig.SAMPLE_SEARCH_RESULTS
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    def text(self, query, max_results=5):
        """Mock text search method."""
        return self.results[:max_results]


def mock_ddgs_context(results=None):
    """Context manager for mocking DDGS."""
    return patch('src.agent.tools.DDGS', return_value=MockDDGS(results))


def create_test_notification_data(topic="test topic", updates=None):
    """Create test notification data."""
    if updates is None:
        updates = TestConfig.SAMPLE_NOTIFICATION_DATA["relevant_updates"]
    
    return {
        "should_send_email": True,
        "reasoning": f"Test notification for {topic}",
        "topic_searched": topic,
        "relevant_updates": updates
    }


def create_test_search_results(count=2):
    """Create test search results."""
    results = []
    for i in range(count):
        results.append({
            "title": f"Test Result {i+1}",
            "url": f"http://test{i+1}.com",
            "snippet": f"This is test result {i+1}"
        })
    return results

