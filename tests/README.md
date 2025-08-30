# Event Action Agent - Test Suite

This directory contains comprehensive tests for the Event Action Agent system.

## 📁 Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── README.md                   # This file
├── test_config.py             # Test configuration and utilities
├── test_agent_integration.py  # Agent integration tests
├── test_cli.py                # CLI functionality tests
├── test_memory_system.py      # Memory system integration tests
├── test_memory_simple.py      # Simple memory system tests
├── test_complete_system.py    # End-to-end system tests
└── run_tests.py               # Test runner script
```

## 🧪 Test Categories

### 1. **Unit Tests**
- `test_agent_integration.py`: Tests individual components and their integration
- `test_cli.py`: Tests CLI functionality and user interactions
- `test_config.py`: Test utilities and configuration

### 2. **Integration Tests**
- `test_memory_system.py`: Tests memory system with real web searches
- `test_memory_simple.py`: Tests memory system with controlled data
- `test_complete_system.py`: End-to-end system integration tests

### 3. **System Tests**
- `run_tests.py`: Comprehensive test runner that tests the entire system

## 🚀 Running Tests

### Run All Tests
```bash
# From the project root
python tests/run_tests.py

# Or from the tests directory
cd tests
python run_tests.py
```

### Run Individual Test Files
```bash
# Run specific test file
python tests/test_memory_system.py
python tests/test_cli.py
python tests/test_agent_integration.py
```

### Run Unit Tests Only
```bash
# From the tests directory
python -m unittest discover -p "test_*.py" -v
```

### Run Specific Test Class
```bash
# Run specific test class
python -m unittest tests.test_agent_integration.TestAgentIntegration -v
```

## 📊 Test Coverage

### Agent Integration Tests
- ✅ Agent initialization
- ✅ Tool availability and functionality
- ✅ Memory system integration
- ✅ Duplicate prevention
- ✅ Notification statistics

### CLI Tests
- ✅ CLI initialization
- ✅ Status display
- ✅ Memory status display
- ✅ Examples display
- ✅ User query handling
- ✅ Memory reset functionality
- ✅ Recent notifications display
- ✅ Agent execution

### Memory System Tests
- ✅ Database initialization
- ✅ Idempotency key generation
- ✅ Duplicate detection
- ✅ Notification tracking
- ✅ Statistics generation
- ✅ History management

### Integration Tests
- ✅ End-to-end workflows
- ✅ Real web search integration
- ✅ Memory system with live data
- ✅ Complete system functionality

## 🔧 Test Configuration

### Environment Setup
Tests automatically set up and tear down test environments:
- Temporary databases for isolation
- Mocked external services
- Clean memory state between tests

### Mocking
- `DDGS` (web search) is mocked to avoid external API calls
- `ChatOpenAI` (LLM) is mocked to avoid API costs
- Database operations use temporary files

### Test Data
- Sample notification data
- Mock search results
- Controlled test scenarios

## 📈 Test Results

### Expected Output
```
🚀 Event Action Agent - Complete Test Suite
============================================================
🧪 Running Unit Tests
==================================================
test_agent_initialization (__main__.TestAgentIntegration) ... ok
test_tools_availability (__main__.TestAgentIntegration) ... ok
...

🔗 Running Integration Tests
==================================================
Running test_memory_system.py...
✅ test_memory_system.py passed
...

🚀 Running System Tests
==================================================
Testing CLI: python main.py --status
✅ CLI test passed
...

============================================================
📊 Test Summary
============================================================
Unit Tests:        ✅ PASSED
Integration Tests: ✅ PASSED
System Tests:      ✅ PASSED

Overall Result:    ✅ ALL TESTS PASSED

🎉 All tests passed! The system is working correctly.
```

## 🛠️ Adding New Tests

### 1. **Unit Tests**
Create a new test file following the pattern `test_*.py`:
```python
import unittest
from unittest.mock import patch

class TestNewFeature(unittest.TestCase):
    def setUp(self):
        # Setup test environment
        pass
    
    def test_new_feature(self):
        # Test the new feature
        pass
```

### 2. **Integration Tests**
Create a script that tests the complete workflow:
```python
#!/usr/bin/env python3
"""
Integration test for new feature.
"""

def test_new_feature_integration():
    # Test the complete workflow
    pass

if __name__ == "__main__":
    test_new_feature_integration()
```

### 3. **Update Test Runner**
Add new tests to `run_tests.py` if needed.

## 🐛 Debugging Tests

### Common Issues
1. **Import Errors**: Ensure parent directory is in Python path
2. **Database Conflicts**: Tests use temporary databases
3. **Mock Issues**: Check that external services are properly mocked

### Debug Mode
```bash
# Run with verbose output
python -m unittest tests.test_agent_integration -v

# Run specific test method
python -m unittest tests.test_agent_integration.TestAgentIntegration.test_agent_initialization -v
```

## 📝 Test Best Practices

1. **Isolation**: Each test should be independent
2. **Cleanup**: Always clean up test data
3. **Mocking**: Mock external dependencies
4. **Descriptive Names**: Use clear test method names
5. **Assertions**: Use specific assertions
6. **Documentation**: Document complex test scenarios

## 🔄 Continuous Integration

The test suite is designed to run in CI/CD environments:
- No external dependencies
- Fast execution
- Clear pass/fail results
- Comprehensive coverage
