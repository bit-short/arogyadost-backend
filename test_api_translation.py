#!/usr/bin/env python3
"""
Test API translation endpoints using curl
"""

import subprocess
import json
import time
import sys

def test_api_translation():
    """Test the API translation functionality"""
    
    print("🧪 Testing API Translation Endpoints")
    print("=" * 50)
    
    # Test English (default)
    print("\n🇺🇸 Testing English (default):")
    print("-" * 30)
    
    try:
        result = subprocess.run([
            'curl', '-s', 
            'http://localhost:8000/api/routines/daily'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data and len(data) > 0:
                print(f"✅ English response received")
                print(f"Step: {data[0]['step']}")
                if data[0]['products']:
                    print(f"Product: {data[0]['products'][0]['name']}")
                    print(f"Description: {data[0]['products'][0]['description']}")
            else:
                print("❌ Empty response")
        else:
            print(f"❌ API call failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error testing English: {e}")
    
    # Test Hindi
    print("\n🇮🇳 Testing Hindi translation:")
    print("-" * 30)
    
    try:
        result = subprocess.run([
            'curl', '-s', 
            '-H', 'Accept-Language: hi',
            'http://localhost:8000/api/routines/daily'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data and len(data) > 0:
                print(f"✅ Hindi response received")
                print(f"Step: {data[0]['step']}")
                if data[0]['products']:
                    print(f"Product: {data[0]['products'][0]['name']}")
                    print(f"Description: {data[0]['products'][0]['description']}")
            else:
                print("❌ Empty response")
        else:
            print(f"❌ API call failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error testing Hindi: {e}")
    
    # Test Tamil
    print("\n🇮🇳 Testing Tamil translation:")
    print("-" * 30)
    
    try:
        result = subprocess.run([
            'curl', '-s', 
            '-H', 'Accept-Language: ta',
            'http://localhost:8000/api/routines/daily'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data and len(data) > 0:
                print(f"✅ Tamil response received")
                print(f"Step: {data[0]['step']}")
                if data[0]['products']:
                    print(f"Product: {data[0]['products'][0]['name']}")
                    print(f"Description: {data[0]['products'][0]['description']}")
            else:
                print("❌ Empty response")
        else:
            print(f"❌ API call failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error testing Tamil: {e}")
    
    print("\n💡 Next Steps:")
    print("1. Start the frontend: cd ../arogyadost-web && npm run dev")
    print("2. Use the language switcher in the UI")
    print("3. Check the Check-in page for translated supplements")

if __name__ == "__main__":
    print("⚠️  Make sure the backend server is running:")
    print("   cd arogyadost-backend && uvicorn main:app --reload")
    print()
    
    # Wait a moment for user to start server
    input("Press Enter when the server is running...")
    
    test_api_translation()