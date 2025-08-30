#!/usr/bin/env python3
"""
Test runner for all Event Action Agent tests.
"""

import sys
import os
import unittest
import subprocess

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_unit_tests():
    """Run all unit tests."""
    print("🧪 Running Unit Tests")
    print("=" * 50)
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def run_integration_tests():
    """Run integration tests."""
    print("\n🔗 Running Integration Tests")
    print("=" * 50)
    
    # Run the integration test scripts
    test_scripts = [
        'test_memory_system.py',
        'test_memory_simple.py',
        'test_complete_system.py'
    ]
    
    success_count = 0
    total_count = len(test_scripts)
    
    for script in test_scripts:
        script_path = os.path.join(os.path.dirname(__file__), script)
        print(f"\nRunning {script}...")
        
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(__file__)
            )
            
            if result.returncode == 0:
                print(f"✅ {script} passed")
                success_count += 1
            else:
                print(f"❌ {script} failed")
                print(f"Error: {result.stderr}")
                
        except Exception as e:
            print(f"❌ {script} failed with exception: {e}")
    
    print(f"\nIntegration Tests: {success_count}/{total_count} passed")
    return success_count == total_count


def run_system_tests():
    """Run system-level tests."""
    print("\n🚀 Running System Tests")
    print("=" * 50)
    
    # Test CLI commands
    cli_tests = [
        ['--status'],
        ['--memory'],
        ['--recent'],
        ['--reset-memory']
    ]
    
    success_count = 0
    total_count = len(cli_tests)
    
    for test_args in cli_tests:
        print(f"\nTesting CLI: python main.py {' '.join(test_args)}")
        
        try:
            result = subprocess.run(
                [sys.executable, 'main.py'] + test_args,
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.dirname(__file__))
            )
            
            if result.returncode == 0:
                print(f"✅ CLI test passed")
                success_count += 1
            else:
                print(f"❌ CLI test failed")
                print(f"Error: {result.stderr}")
                
        except Exception as e:
            print(f"❌ CLI test failed with exception: {e}")
    
    print(f"\nSystem Tests: {success_count}/{total_count} passed")
    return success_count == total_count


def main():
    """Main test runner."""
    print("🚀 Event Action Agent - Complete Test Suite")
    print("=" * 60)
    
    # Run all test types
    unit_success = run_unit_tests()
    integration_success = run_integration_tests()
    system_success = run_system_tests()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"Unit Tests:        {'✅ PASSED' if unit_success else '❌ FAILED'}")
    print(f"Integration Tests: {'✅ PASSED' if integration_success else '❌ FAILED'}")
    print(f"System Tests:      {'✅ PASSED' if system_success else '❌ FAILED'}")
    
    overall_success = unit_success and integration_success and system_success
    print(f"\nOverall Result:    {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n🎉 All tests passed! The system is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the output above.")
    
    return overall_success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
