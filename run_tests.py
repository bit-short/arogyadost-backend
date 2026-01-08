#!/usr/bin/env python3
"""
Simple test runner for Aarogyadost Backend
Run with: python run_tests.py
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n🧪 {description}")
    print("=" * 50)
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print("✅ PASSED")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False

def main():
    """Run all tests"""
    print("🚀 Running Aarogyadost Backend Tests")
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Please run from the project root directory")
        sys.exit(1)
    
    tests_passed = 0
    total_tests = 0
    
    # Test commands to run
    test_commands = [
        ("python -m pytest tests/ -v", "Running pytest tests"),
        ("python -c 'import main; print(\"✅ Main module imports successfully\")'", "Testing main module import"),
        ("python -c 'import requests; print(\"✅ Dependencies available\")'", "Checking dependencies"),
    ]
    
    for cmd, description in test_commands:
        total_tests += 1
        if run_command(cmd, description):
            tests_passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Summary: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
