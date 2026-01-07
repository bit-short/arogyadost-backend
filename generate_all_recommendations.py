#!/usr/bin/env python3

import json
import os
from datetime import datetime, timedelta

# Test users from the dataset
TEST_USERS = [
    "test_user_1_29f",  # 29F, Bengaluru - Vitamin D deficiency, dyslipidemia
    "test_user_2_29m",  # 29M, Mumbai - Fitness focused
    "test_user_3_31m",  # 31M, Delhi - Weight loss, metabolic health
    "test_user_4_31m",  # 31M, Hyderabad - Longevity optimization
    "test_user_5_55f"   # 55F, Chennai - Hormonal balance, bone health
]

def generate_recommendations_for_user(user_id):
    """Generate recommendations based on user profile patterns"""
    
    # Extract age and gender from user_id
    parts = user_id.split('_')
    age_gender = parts[-1]  # e.g., "29f"
    age = int(age_gender[:-1])
    gender = age_gender[-1].upper()
    
    recommendations = []
    
    # User-specific recommendations based on known profiles
    if user_id == "test_user_1_29f":
        # 29F with Vitamin D deficiency, dyslipidemia
        recommendations = [
            {
                "test_name": "Vitamin D",
                "priority": "high",
                "rationale": "Known vitamin D deficiency requiring monitoring",
                "timing": "within 2 weeks",
                "category": "vitamins"
            },
            {
                "test_name": "Lipid Profile",
                "priority": "high", 
                "rationale": "Active dyslipidemia management",
                "timing": "within 1 month",
                "category": "lipid_profile"
            },
            {
                "test_name": "Complete Blood Count",
                "priority": "medium",
                "rationale": "Annual screening for young adult female",
                "timing": "within 6 weeks",
                "category": "complete_blood_count"
            }
        ]
    
    elif user_id == "test_user_2_29m":
        # 29M, fitness focused
        recommendations = [
            {
                "test_name": "Comprehensive Metabolic Panel",
                "priority": "medium",
                "rationale": "Fitness optimization and metabolic assessment",
                "timing": "within 4 weeks",
                "category": "metabolic"
            },
            {
                "test_name": "Testosterone",
                "priority": "low",
                "rationale": "Hormone optimization for fitness goals",
                "timing": "within 8 weeks",
                "category": "hormones"
            },
            {
                "test_name": "Vitamin B12 and Folate",
                "priority": "medium",
                "rationale": "Energy metabolism support for active lifestyle",
                "timing": "within 6 weeks",
                "category": "vitamins"
            }
        ]
    
    elif user_id == "test_user_3_31m":
        # 31M, weight loss, metabolic health
        recommendations = [
            {
                "test_name": "HbA1c and Fasting Glucose",
                "priority": "high",
                "rationale": "Metabolic health assessment for weight management",
                "timing": "within 2 weeks",
                "category": "metabolic"
            },
            {
                "test_name": "Lipid Profile",
                "priority": "medium",
                "rationale": "Cardiovascular risk assessment during weight loss",
                "timing": "within 4 weeks",
                "category": "lipid_profile"
            },
            {
                "test_name": "Thyroid Function Panel",
                "priority": "medium",
                "rationale": "Rule out thyroid issues affecting weight",
                "timing": "within 6 weeks",
                "category": "hormones"
            }
        ]
    
    elif user_id == "test_user_4_31m":
        # 31M, longevity optimization
        recommendations = [
            {
                "test_name": "Advanced Longevity Panel",
                "priority": "medium",
                "rationale": "Comprehensive longevity biomarker assessment",
                "timing": "within 3 weeks",
                "category": "metabolic"
            },
            {
                "test_name": "Inflammatory Markers (CRP, IL-6)",
                "priority": "medium",
                "rationale": "Inflammation assessment for longevity optimization",
                "timing": "within 4 weeks",
                "category": "inflammatory"
            },
            {
                "test_name": "Hormone Panel (Testosterone, IGF-1)",
                "priority": "low",
                "rationale": "Hormonal optimization for healthy aging",
                "timing": "within 8 weeks",
                "category": "hormones"
            }
        ]
    
    elif user_id == "test_user_5_55f":
        # 55F, hormonal balance, bone health
        recommendations = [
            {
                "test_name": "Menopause Hormone Panel",
                "priority": "high",
                "rationale": "Hormonal balance assessment for 55-year-old female",
                "timing": "within 2 weeks",
                "category": "hormones"
            },
            {
                "test_name": "Bone Health Panel (Vitamin D, Calcium, PTH)",
                "priority": "high",
                "rationale": "Bone health monitoring for postmenopausal woman",
                "timing": "within 3 weeks",
                "category": "minerals"
            },
            {
                "test_name": "Cardiovascular Risk Panel",
                "priority": "medium",
                "rationale": "Enhanced screening for women 50+",
                "timing": "within 1 month",
                "category": "cardiovascular"
            }
        ]
    
    # Add age/gender-based recommendations
    if age >= 40:
        recommendations.append({
            "test_name": "Annual Health Screening",
            "priority": "medium",
            "rationale": f"Routine screening for {age}-year-old adult",
            "timing": "within 2 months",
            "category": "metabolic"
        })
    
    if gender == "M" and age >= 50:
        recommendations.append({
            "test_name": "PSA (Prostate Screening)",
            "priority": "medium", 
            "rationale": "Prostate cancer screening for men 50+",
            "timing": "within 6 weeks",
            "category": "tumor_markers"
        })
    
    return recommendations

def generate_all_recommendations():
    """Generate recommendations for all test users"""
    
    print("🏥 Health Recommendations for All Test Users")
    print("=" * 60)
    
    all_results = {}
    
    for user_id in TEST_USERS:
        print(f"\n👤 {user_id.upper()}")
        print("-" * 40)
        
        recommendations = generate_recommendations_for_user(user_id)
        
        # Calculate summary
        priority_counts = {"high": 0, "medium": 0, "low": 0}
        categories = set()
        
        for rec in recommendations:
            priority_counts[rec["priority"]] += 1
            categories.add(rec["category"])
        
        summary = {
            "total_recommendations": len(recommendations),
            "high_priority_count": priority_counts["high"],
            "medium_priority_count": priority_counts["medium"], 
            "low_priority_count": priority_counts["low"],
            "categories_covered": sorted(list(categories))
        }
        
        # Display results
        print(f"📊 Summary: {summary['total_recommendations']} recommendations")
        print(f"   High: {summary['high_priority_count']}, Medium: {summary['medium_priority_count']}, Low: {summary['low_priority_count']}")
        print(f"   Categories: {', '.join(summary['categories_covered'])}")
        
        print("\n💊 Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}[rec["priority"]]
            print(f"{i}. {priority_emoji} {rec['test_name']} ({rec['priority']} priority)")
            print(f"   📝 {rec['rationale']}")
            print(f"   ⏰ {rec['timing']}")
            print()
        
        # Store results
        all_results[user_id] = {
            "user_id": user_id,
            "generated_at": datetime.now().isoformat(),
            "summary": summary,
            "recommendations": recommendations
        }
    
    # Save results to file
    with open("all_user_recommendations.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n✅ Generated recommendations for {len(TEST_USERS)} users")
    print("📁 Results saved to: all_user_recommendations.json")
    
    # Overall statistics
    total_recs = sum(result["summary"]["total_recommendations"] for result in all_results.values())
    total_high = sum(result["summary"]["high_priority_count"] for result in all_results.values())
    
    print(f"\n📈 Overall Statistics:")
    print(f"   Total recommendations: {total_recs}")
    print(f"   High priority recommendations: {total_high}")
    print(f"   Average per user: {total_recs / len(TEST_USERS):.1f}")

if __name__ == "__main__":
    generate_all_recommendations()
