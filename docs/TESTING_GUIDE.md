# Event Action Agent - Testing Guide

## 🧪 **Complete Testing Guide**

This guide shows you all the different ways to run tests with the improved project structure.

## 🚀 **Quick Start**

### **1. Install Dependencies**
```bash
# Install all dependencies including pytest
pip install -r requirements.txt

# Or install pytest separately
pip install pytest
```

### **2. Run All Tests**
```bash
# Using the test runner script (recommended)
python scripts/run_tests.py

# Using pytest directly
python -m pytest tests/ -v

# Using unittest
python -m unittest discover tests/ -v
```

## 📋 **Test Categories**

### **Unit Tests** (Individual Components)
- Agent initialization and configuration
- Tool functionality (search_web, checkIsMailneedtoSend)
- Memory system operations
- CLI functionality

### **Integration Tests** (Component Interactions)
- Agent with tools integration
- Memory system with tools
- CLI with agent integration

### **System Tests** (End-to-End)
- Complete workflow testing
- CLI command execution
- Real agent execution

## 🛠️ **Different Ways to Run Tests**

### **1. Using the Test Runner Script (Recommended)**
```bash
# Run all tests with detailed output
python scripts/run_tests.py

# This runs:
# - Unit tests (20 tests)
# - Integration tests (3 tests)  
# - System tests (4 tests)
```

### **2. Using pytest (Modern Python Testing)**
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_memory_system.py -v

# Run specific test function
python -m pytest tests/test_agent_integration.py::TestAgentIntegration::test_agent_initialization -v

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run tests with shorter output
python -m pytest tests/ -v --tb=short

# Run tests and stop on first failure
python -m pytest tests/ -x
```

### **3. Using unittest (Python Standard Library)**
```bash
# Run all tests
python -m unittest discover tests/ -v

# Run specific test file
python -m unittest tests.test_memory_system -v

# Run specific test class
python -m unittest tests.test_agent_integration.TestAgentIntegration -v
```

### **4. Running Individual Test Files**
```bash
# Direct execution of test files
python tests/test_memory_simple.py
python tests/test_memory_system.py
python tests/test_complete_system.py
python tests/test_agent_integration.py
python tests/test_cli.py
```

## 📊 **Test Results Interpretation**

### **✅ Successful Test Run**
```
============================================= 26 passed, 1 warning ======================================
```
- All tests passed
- 1 warning (deprecation warning, not critical)

### **❌ Failed Test Run**
```
============================================= 1 failed, 25 passed ======================================
```
- Some tests failed
- Check the error details

### **⚠️ Test with Warnings**
```
============================================= 26 passed, 1 warning ======================================
```
- Tests passed but with warnings
- Usually deprecation warnings

## 🎯 **Specific Test Examples**

### **Memory System Tests**
```bash
# Test memory system functionality
python -m pytest tests/test_memory_system.py -v

# Test simple memory operations
python -m pytest tests/test_memory_simple.py -v
```

### **Agent Integration Tests**
```bash
# Test agent with all tools
python -m pytest tests/test_agent_integration.py -v

# Test specific agent functionality
python -m pytest tests/test_agent_integration.py::TestAgentIntegration::test_agent_initialization -v
```

### **CLI Tests**
```bash
# Test CLI functionality
python -m pytest tests/test_cli.py -v

# Test specific CLI features
python -m pytest tests/test_cli.py::TestCLI::test_show_status -v
```

### **Complete System Tests**
```bash
# Test end-to-end functionality
python -m pytest tests/test_complete_system.py -v
```

## 🔧 **Test Configuration**

### **pytest Configuration**
Create `pytest.ini` in the project root:
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### **Test Environment**
Tests use:
- Mocked external dependencies (DDGS, ChatOpenAI)
- Temporary databases for memory tests
- Isolated test environment

## 📈 **Test Coverage**

### **Current Coverage**
- **Unit Tests**: 20 tests covering individual components
- **Integration Tests**: 3 tests covering component interactions
- **System Tests**: 4 tests covering end-to-end workflows

### **Coverage Areas**
- ✅ Agent initialization and configuration
- ✅ Tool functionality (search_web, checkIsMailneedtoSend)
- ✅ Memory system operations
- ✅ CLI functionality
- ✅ Import path handling
- ✅ Error handling

## 🚨 **Troubleshooting**

### **Import Errors**
```bash
# If you get import errors, make sure you're in the project root
cd /path/to/event-action-agent

# And activate the virtual environment
source .venv/bin/activate
```

### **pytest Not Found**
```bash
# Install pytest
pip install pytest

# Or install all requirements
pip install -r requirements.txt
```

### **Test Failures**
```bash
# Run with verbose output to see details
python -m pytest tests/ -v -s

# Run specific failing test
python -m pytest tests/test_specific.py -v -s
```

## 🎉 **Best Practices**

### **1. Run Tests Before Committing**
```bash
# Always run the full test suite
python scripts/run_tests.py
```

### **2. Use pytest for Development**
```bash
# Quick test runs during development
python -m pytest tests/test_specific.py -v
```

### **3. Check Coverage Regularly**
```bash
# Run with coverage report
python -m pytest tests/ --cov=src --cov-report=html
```

### **4. Fix Warnings**
```bash
# Run with warnings as errors
python -m pytest tests/ -W error::DeprecationWarning
```

## 📚 **Additional Resources**

- [pytest Documentation](https://docs.pytest.org/)
- [unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [Python Testing Best Practices](https://realpython.com/python-testing/)

## 🎯 **Summary**

The Event Action Agent has a comprehensive testing suite with multiple ways to run tests:

1. **`python scripts/run_tests.py`** - Complete test suite (recommended)
2. **`python -m pytest tests/ -v`** - Modern pytest approach
3. **`python -m unittest discover tests/ -v`** - Standard library approach
4. **Individual test files** - Direct execution

All tests are passing and the system is fully functional with the new structure! 🚀
