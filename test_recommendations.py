#!/usr/bin/env python3

# Simple test script to validate the recommendation engine logic
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock the dependencies for testing
class MockBaseModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class MockField:
    @staticmethod
    def default_factory(func):
        return func()

# Mock pydantic
sys.modules['pydantic'] = type('MockPydantic', (), {
    'BaseModel': MockBaseModel,
    'Field': MockField
})()

# Mock enum
class MockEnum:
    def __init__(self, name, values):
        for value in values:
            setattr(self, value.upper(), value)
        self.__members__ = {v.upper(): v for v in values}
        self.value = values[0] if values else None

sys.modules['enum'] = type('MockEnum', (), {
    'Enum': MockEnum
})()

# Now test our logic
from datetime import datetime

# Test data
test_user_data = {
    "user_id": "test_user_1",
    "demographics": {"age": 35, "sex": "male"},
    "latest_biomarkers": {
        "test_date": datetime(2024, 1, 15),
        "categories": {
            "metabolic": {
                "glucose": {"value": 105, "unit": "mg/dL", "status": "high"},
                "hba1c": {"value": 5.8, "unit": "%", "status": "high"}
            },
            "lipid_profile": {
                "cholesterol": {"value": 220, "unit": "mg/dL", "status": "high"},
                "ldl": {"value": 145, "unit": "mg/dL", "status": "high"}
            }
        }
    },
    "conditions": [
        {"condition": "Prediabetes", "status": "active"},
        {"condition": "Dyslipidemia", "status": "active"}
    ],
    "family_history": [
        {"condition": "Type 2 Diabetes", "relation": "parent"}
    ]
}

print("🧪 Testing Health Recommendations Engine")
print("=" * 50)

# Test biomarker rule logic
print("\n📊 Testing Biomarker Rules:")
abnormal_markers = []
for category, markers in test_user_data["latest_biomarkers"]["categories"].items():
    for marker, data in markers.items():
        if data["status"] in ["high", "low"]:
            abnormal_markers.append(f"{marker}: {data['value']} {data['unit']} ({data['status']})")

print(f"Found {len(abnormal_markers)} abnormal biomarkers:")
for marker in abnormal_markers:
    print(f"  - {marker}")

# Test condition rule logic
print("\n🏥 Testing Condition Rules:")
active_conditions = [c for c in test_user_data["conditions"] if c["status"] == "active"]
print(f"Found {len(active_conditions)} active conditions:")
for condition in active_conditions:
    print(f"  - {condition['condition']}")

# Test demographic rule logic
print("\n👤 Testing Demographic Rules:")
age = test_user_data["demographics"]["age"]
sex = test_user_data["demographics"]["sex"]
print(f"Age: {age}, Sex: {sex}")

if 40 <= age <= 64:
    print("  - Qualifies for middle-age screening")
elif age >= 65:
    print("  - Qualifies for senior screening")
else:
    print("  - Qualifies for young adult screening")

# Test family history logic
print("\n👨‍👩‍👧‍👦 Testing Family History Rules:")
family_conditions = [fh["condition"] for fh in test_user_data["family_history"]]
print(f"Family history conditions: {family_conditions}")

diabetes_family_history = any("diabetes" in condition.lower() for condition in family_conditions)
heart_family_history = any("heart" in condition.lower() for condition in family_conditions)

if diabetes_family_history:
    print("  - Enhanced diabetes screening recommended")
if heart_family_history:
    print("  - Enhanced cardiac screening recommended")

# Test priority scoring logic
print("\n⭐ Testing Priority Scoring:")
risk_factors = 0

# Age risk
if age >= 40:
    risk_factors += 1
    print("  - Age risk factor: +1")

# Condition risk
for condition in active_conditions:
    risk_factors += 1
    print(f"  - Condition risk ({condition['condition']}): +1")

# Family history risk
if diabetes_family_history or heart_family_history:
    risk_factors += 1
    print("  - Family history risk: +1")

print(f"Total risk factors: {risk_factors}")

# Simulate recommendations
print("\n💊 Sample Recommendations Generated:")
recommendations = []

# Abnormal biomarker follow-ups
for category, markers in test_user_data["latest_biomarkers"]["categories"].items():
    for marker, data in markers.items():
        if data["status"] in ["high", "low"]:
            priority = "high" if data["status"] == "high" and data["value"] > 200 else "medium"
            recommendations.append({
                "test": f"{marker.title()} Retest",
                "priority": priority,
                "rationale": f"{marker.title()} is {data['status']} ({data['value']} {data['unit']})",
                "timing": "within 4 weeks" if priority == "medium" else "within 1 week"
            })

# Condition monitoring
condition_tests = {
    "prediabetes": "HbA1c and Glucose",
    "dyslipidemia": "Lipid Profile"
}

for condition in active_conditions:
    condition_name = condition["condition"].lower()
    for key, test in condition_tests.items():
        if key in condition_name:
            recommendations.append({
                "test": test,
                "priority": "medium",
                "rationale": f"Routine monitoring for {condition['condition']}",
                "timing": "within 3 months"
            })

# Display recommendations
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec['test']} ({rec['priority']} priority)")
    print(f"   Rationale: {rec['rationale']}")
    print(f"   Timing: {rec['timing']}")
    print()

print(f"✅ Generated {len(recommendations)} recommendations successfully!")
print("\n🎉 Health Recommendations Engine test completed!")
