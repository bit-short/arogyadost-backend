#!/usr/bin/env python3
"""
Simple functional tests for Aarogyadost Backend
Tests core functionality without requiring server startup
"""

import json
import os
import sys

def test_user_data_files():
    """Test that user data files exist and are valid JSON"""
    users_path = 'datasets/users'
    if not os.path.exists(users_path):
        print("❌ Users dataset directory not found")
        return False
    
    user_files = [f for f in os.listdir(users_path) if f.endswith('.json')]
    
    if len(user_files) == 0:
        print("❌ No user JSON files found")
        return False
    
    valid_files = 0
    for user_file in user_files:
        try:
            with open(os.path.join(users_path, user_file), 'r') as f:
                data = json.load(f)
                if 'user_id' in data and 'demographics' in data:
                    valid_files += 1
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in {user_file}")
        except Exception as e:
            print(f"❌ Error reading {user_file}: {e}")
    
    print(f"✅ Found {valid_files}/{len(user_files)} valid user data files")
    return valid_files > 0

def test_biomarker_data():
    """Test biomarker data structure"""
    biomarkers_path = 'datasets/biomarkers'
    if not os.path.exists(biomarkers_path):
        print("❌ Biomarkers dataset directory not found")
        return False
    
    biomarker_files = [f for f in os.listdir(biomarkers_path) if f.endswith('.json')]
    
    if len(biomarker_files) == 0:
        print("❌ No biomarker JSON files found")
        return False
    
    valid_files = 0
    for bio_file in biomarker_files:
        try:
            with open(os.path.join(biomarkers_path, bio_file), 'r') as f:
                data = json.load(f)
                if isinstance(data, dict) and len(data) > 0:
                    valid_files += 1
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in {bio_file}")
        except Exception as e:
            print(f"❌ Error reading {bio_file}: {e}")
    
    print(f"✅ Found {valid_files}/{len(biomarker_files)} valid biomarker files")
    return valid_files > 0

def test_config_files():
    """Test configuration files"""
    config_files = [
        'config/llm_config.json'
    ]
    
    valid_configs = 0
    for config_file in config_files:
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        valid_configs += 1
                        print(f"✅ Valid config: {config_file}")
            except json.JSONDecodeError:
                print(f"❌ Invalid JSON in {config_file}")
            except Exception as e:
                print(f"❌ Error reading {config_file}: {e}")
        else:
            print(f"⚠️  Config file not found: {config_file}")
    
    return valid_configs > 0

def test_documentation_files():
    """Test that documentation files exist"""
    doc_files = [
        'README.md',
        'docs/API_DOCUMENTATION.md',
        'docs/DEPLOYMENT.md'
    ]
    
    found_docs = 0
    for doc_file in doc_files:
        if os.path.exists(doc_file):
            try:
                with open(doc_file, 'r') as f:
                    content = f.read()
                    if len(content) > 100:  # Basic content check
                        found_docs += 1
                        print(f"✅ Found documentation: {doc_file}")
            except Exception as e:
                print(f"❌ Error reading {doc_file}: {e}")
        else:
            print(f"⚠️  Documentation not found: {doc_file}")
    
    return found_docs > 0

def main():
    """Run all functional tests"""
    print("🧪 Running Aarogyadost Backend Functional Tests")
    print("=" * 50)
    
    tests = [
        test_user_data_files,
        test_biomarker_data,
        test_config_files,
        test_documentation_files
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print(f"\n🔍 Running {test.__name__}...")
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Functional Test Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All functional tests passed!")
        return 0
    else:
        print("⚠️  Some functional tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
