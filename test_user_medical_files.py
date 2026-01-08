#!/usr/bin/env python3
"""
Test script to verify user-specific medical files functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.user_context import UserContextManager

def test_user_medical_files():
    """Test that medical files are returned for different users."""
    
    # Initialize user context manager
    user_manager = UserContextManager()
    
    print("=== Testing User Medical Files ===\n")
    
    # Test hardcoded user
    print("1. Testing hardcoded user:")
    user_manager.select_user("hardcoded")
    hardcoded_files = user_manager.get_user_medical_files()
    print(f"   Hardcoded user files: {len(hardcoded_files)} files")
    if hardcoded_files:
        print(f"   First file: {hardcoded_files[0]['filename']}")
    
    # Test dataset user
    print("\n2. Testing test_user_1_29f:")
    try:
        user_manager.select_user("test_user_1_29f")
        test_user_files = user_manager.get_user_medical_files()
        print(f"   Test user files: {len(test_user_files)} files")
        if test_user_files:
            for i, file in enumerate(test_user_files):
                print(f"   File {i+1}: {file['filename']} - {file['summary']}")
        else:
            print("   No files found for test user")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test available users
    print("\n3. Available users:")
    users = user_manager.get_available_users()
    for user in users:
        print(f"   - {user.user_id}: {user.display_name} (completeness: {user.data_availability.completeness_score:.1f}%)")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_user_medical_files()