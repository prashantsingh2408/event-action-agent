#!/usr/bin/env python3
"""
Test runner for Event Action Agent.
Run this from the project root to execute all tests.
"""

import subprocess
import sys
import os

def main():
    """Run all tests."""
    print("🚀 Running Event Action Agent Tests")
    print("=" * 50)
    
    # Get the path to the tests directory
    tests_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests')
    
    # Run the test runner
    result = subprocess.run([sys.executable, 'run_tests.py'], cwd=tests_dir)
    
    return result.returncode

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
