#!/usr/bin/env python3

import asyncio
import json

def test_user_selection_system():
    """Test the user selection system functionality."""
    
    print("👥 Testing User Selection System")
    print("=" * 50)
    
    # Test 1: User Context Manager
    print("\n📋 Test 1: User Context Manager")
    
    try:
        from app.services.user_context import UserContextManager
        
        # Initialize manager
        manager = UserContextManager("datasets")
        
        print("✅ User Context Manager initialized")
        print(f"   Default active user: {manager.active_user_id}")
        
        # Test getting available users
        users = manager.get_available_users()
        print(f"   Total users loaded: {len(users)}")
        
        # Show user summary
        for user in users:
            print(f"   - {user.user_id}: {user.display_name}")
            print(f"     Age: {user.demographics.age}, Gender: {user.demographics.gender}")
            print(f"     Data completeness: {user.data_availability.completeness_score:.1f}%")
            print(f"     Hardcoded: {user.is_hardcoded}")
            print()
        
    except Exception as e:
        print(f"❌ User Context Manager test failed: {e}")
        return
    
    # Test 2: User Selection
    print("🎯 Test 2: User Selection")
    
    try:
        # Test selecting hardcoded user
        hardcoded_user = manager.select_user("hardcoded")
        print(f"✅ Selected hardcoded user: {hardcoded_user.display_name}")
        
        # Test selecting dataset user
        dataset_users = [u for u in users if not u.is_hardcoded]
        if dataset_users:
            test_user = dataset_users[0]
            selected_user = manager.select_user(test_user.user_id)
            print(f"✅ Selected dataset user: {selected_user.display_name}")
            
            # Test getting current user
            current_user = manager.get_current_user()
            print(f"✅ Current user confirmed: {current_user.user_id}")
        
        # Test invalid user selection
        try:
            manager.select_user("invalid_user_id")
            print("❌ Should have failed for invalid user ID")
        except ValueError as e:
            print(f"✅ Correctly rejected invalid user ID: {str(e)[:50]}...")
        
    except Exception as e:
        print(f"❌ User selection test failed: {e}")
        return
    
    # Test 3: Data Availability Checking
    print("\n📊 Test 3: Data Availability Checking")
    
    try:
        for user in users[:3]:  # Test first 3 users
            availability = user.data_availability
            print(f"📁 {user.user_id}:")
            print(f"   Biomarkers: {'✅' if availability.biomarkers else '❌'}")
            print(f"   Medical History: {'✅' if availability.medical_history else '❌'}")
            print(f"   Lifestyle: {'✅' if availability.lifestyle else '❌'}")
            print(f"   AI Interactions: {'✅' if availability.ai_interactions else '❌'}")
            print(f"   Interventions: {'✅' if availability.interventions else '❌'}")
            print(f"   Completeness: {availability.completeness_score:.1f}%")
            print()
        
        print("✅ Data availability checking working")
        
    except Exception as e:
        print(f"❌ Data availability test failed: {e}")
        return
    
    # Test 4: User Profile Models
    print("🏗️ Test 4: User Profile Models")
    
    try:
        from app.models.user_profile import UserProfile, Demographics, HealthProfile
        
        # Test model creation
        test_demographics = Demographics(age=30, gender="F")
        test_health = HealthProfile(bmi=22.5, blood_type="A+")
        
        print("✅ Pydantic models working correctly")
        print(f"   Demographics: Age {test_demographics.age}, Gender {test_demographics.gender}")
        print(f"   Health Profile: BMI {test_health.bmi}, Blood Type {test_health.blood_type}")
        
    except Exception as e:
        print(f"❌ User profile models test failed: {e}")
        return
    
    # Test 5: API Response Simulation
    print("\n🌐 Test 5: API Response Simulation")
    
    try:
        from app.models.user_profile import UserSelectionResponse, CurrentUserResponse
        
        # Simulate API responses
        selection_response = UserSelectionResponse(
            users=users,
            total_count=len(users),
            hardcoded_user_id="hardcoded"
        )
        
        current_response = CurrentUserResponse(
            active_user=manager.get_current_user(),
            is_default=manager.is_hardcoded_user_active()
        )
        
        print("✅ API response models working")
        print(f"   Available users: {selection_response.total_count}")
        print(f"   Current user: {current_response.active_user.user_id}")
        print(f"   Is default: {current_response.is_default}")
        
    except Exception as e:
        print(f"❌ API response simulation failed: {e}")
        return
    
    # Test 6: User Categories Analysis
    print("\n📈 Test 6: User Categories Analysis")
    
    try:
        hardcoded_users = [u for u in users if u.is_hardcoded]
        dataset_users = [u for u in users if not u.is_hardcoded]
        
        print(f"📊 User Categories:")
        print(f"   Hardcoded users: {len(hardcoded_users)}")
        print(f"   Dataset users: {len(dataset_users)}")
        
        # Analyze data completeness
        if dataset_users:
            completeness_scores = [u.data_availability.completeness_score for u in dataset_users]
            avg_completeness = sum(completeness_scores) / len(completeness_scores)
            print(f"   Average data completeness: {avg_completeness:.1f}%")
            
            # Find users with full data
            complete_users = [u for u in dataset_users if u.data_availability.completeness_score == 100.0]
            print(f"   Users with complete data: {len(complete_users)}")
            
            # Show age/gender distribution
            ages = [u.demographics.age for u in dataset_users]
            genders = [u.demographics.gender for u in dataset_users]
            
            if ages:
                print(f"   Age range: {min(ages)}-{max(ages)} years")
            
            gender_counts = {}
            for gender in genders:
                gender_counts[gender] = gender_counts.get(gender, 0) + 1
            print(f"   Gender distribution: {gender_counts}")
        
        print("✅ User categories analysis completed")
        
    except Exception as e:
        print(f"❌ User categories analysis failed: {e}")
        return
    
    print("\n🎉 User Selection System Test Completed!")
    print("\n📊 Test Summary:")
    print("✅ User Context Manager initialization")
    print("✅ User loading from datasets and hardcoded data")
    print("✅ User selection and validation")
    print("✅ Data availability checking")
    print("✅ Pydantic model validation")
    print("✅ API response model compatibility")
    print("✅ User categories and analytics")
    
    print(f"\n🎯 Ready for API testing:")
    print("   GET /api/users/available - List all users")
    print("   POST /api/users/select - Select active user")
    print("   GET /api/users/current - Get current user")
    print("   GET /static/user-selection.html - User selection UI")

if __name__ == "__main__":
    test_user_selection_system()
