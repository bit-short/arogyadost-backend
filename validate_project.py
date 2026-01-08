#!/usr/bin/env python3
"""
Simple validation tests for Aarogyadost Backend
Tests basic functionality without requiring full dependencies
"""

import json
import os
import sys

def test_project_structure():
    """Test that key project files exist"""
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'tests/',
        'app/',
        'datasets/'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ Project structure is valid")
    return True

def test_main_py_syntax():
    """Test that main.py has valid Python syntax"""
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        # Try to compile the code
        compile(content, 'main.py', 'exec')
        print("✅ main.py has valid Python syntax")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in main.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading main.py: {e}")
        return False

def test_requirements_file():
    """Test that requirements.txt is readable"""
    try:
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
        
        if len(lines) == 0:
            print("❌ requirements.txt is empty")
            return False
        
        print(f"✅ requirements.txt contains {len(lines)} dependencies")
        return True
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def test_datasets_structure():
    """Test that datasets directory has expected structure"""
    try:
        datasets_path = 'datasets'
        if not os.path.exists(datasets_path):
            print("❌ datasets/ directory not found")
            return False
        
        subdirs = [d for d in os.listdir(datasets_path) 
                  if os.path.isdir(os.path.join(datasets_path, d))]
        
        expected_dirs = ['users', 'biomarkers', 'lifestyle', 'medical_history']
        found_dirs = [d for d in expected_dirs if d in subdirs]
        
        print(f"✅ Found {len(found_dirs)}/{len(expected_dirs)} expected dataset directories")
        return len(found_dirs) > 0
    except Exception as e:
        print(f"❌ Error checking datasets: {e}")
        return False

def test_app_structure():
    """Test that app directory has expected structure"""
    try:
        app_path = 'app'
        if not os.path.exists(app_path):
            print("❌ app/ directory not found")
            return False
        
        subdirs = [d for d in os.listdir(app_path) 
                  if os.path.isdir(os.path.join(app_path, d))]
        
        expected_dirs = ['models', 'routers', 'services']
        found_dirs = [d for d in expected_dirs if d in subdirs]
        
        print(f"✅ Found {len(found_dirs)}/{len(expected_dirs)} expected app directories")
        return len(found_dirs) > 0
    except Exception as e:
        print(f"❌ Error checking app structure: {e}")
        return False

def main():
    """Run all validation tests"""
    print("🧪 Running Aarogyadost Backend Validation Tests")
    print("=" * 50)
    
    tests = [
        test_project_structure,
        test_main_py_syntax,
        test_requirements_file,
        test_datasets_structure,
        test_app_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Validation Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All validation tests passed!")
        return 0
    else:
        print("⚠️  Some validation tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
