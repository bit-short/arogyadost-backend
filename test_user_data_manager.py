#!/usr/bin/env python3
"""
Test script for the in-memory user data manager.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.user_data_manager import user_data_manager


def test_user_data_manager():
    """Test the user data manager functionality."""
    print("🧪 Testing User Data Manager")
    print("=" * 50)
    
    # Test 1: Get all user IDs
    user_ids = user_data_manager.get_all_user_ids()
    print(f"✅ Found {len(user_ids)} users: {user_ids}")
    
    # Test 2: Test each user
    for user_id in user_ids:
        print(f"\n🔍 Testing user: {user_id}")
        
        # Get user summary
        summary = user_data_manager.get_user_summary(user_id)
        if summary:
            print(f"   Display Name: {summary['display_name']}")
            print(f"   Data Completeness: {summary['data_completeness']:.1f}%")
            print(f"   Has Biomarkers: {summary['has_biomarkers']}")
            print(f"   Has Lifestyle: {summary['has_lifestyle']}")
            print(f"   Has Medical History: {summary['has_medical_history']}")
        
        # Test biomarkers
        biomarkers = user_data_manager.get_user_biomarkers(user_id)
        if biomarkers:
            biomarker_count = len(biomarkers) if isinstance(biomarkers, dict) else 0
            print(f"   Biomarkers: {biomarker_count} entries")
        
        # Test lifestyle
        lifestyle = user_data_manager.get_user_lifestyle(user_id)
        if lifestyle:
            print(f"   Lifestyle: Available")
        
        # Test medical history
        medical_history = user_data_manager.get_user_medical_history(user_id)
        if medical_history:
            conditions = len(medical_history.get("conditions", []))
            supplements = len(medical_history.get("supplements", []))
            print(f"   Medical History: {conditions} conditions, {supplements} supplements")
    
    print("\n" + "=" * 50)
    print("🎉 User Data Manager test completed!")


if __name__ == "__main__":
    test_user_data_manager()
