"""
Generate frontend-compatible data from OCR user biomarkers.
"""

from typing import Dict, List, Any
from app.services.user_db_service import user_db_service


def get_health_score(status_counts: Dict[str, int]) -> int:
    """Calculate health score from biomarker statuses."""
    total = sum(status_counts.values())
    if total == 0:
        return 85  # Default good score if no data
    normal = status_counts.get('normal', 0)
    # Also count None/unknown as normal
    unknown = status_counts.get(None, 0) + status_counts.get('unknown', 0)
    return int(((normal + unknown) / total) * 100)


def generate_health_categories(user_id: str) -> List[Dict[str, Any]]:
    """Generate health categories from user biomarkers."""
    biomarkers = user_db_service.get_user_biomarkers_by_category(user_id)
    if not biomarkers:
        return []
    
    category_config = {
        'metabolic': {'name': 'Metabolic Health', 'icon': 'Activity'},
        'lipids': {'name': 'Cardiovascular', 'icon': 'Heart'},
        'vitamins': {'name': 'Nutritional Status', 'icon': 'Pill'},
        'thyroid': {'name': 'Hormonal Balance', 'icon': 'Zap'},
        'liver': {'name': 'Liver Function', 'icon': 'Shield'},
        'kidney': {'name': 'Kidney Function', 'icon': 'Droplet'},
        'cbc': {'name': 'Blood Health', 'icon': 'Droplets'},
        'iron': {'name': 'Iron Status', 'icon': 'Flame'},
    }
    
    categories = []
    for cat, markers in biomarkers.items():
        if cat not in category_config:
            continue
        
        status_counts = {'normal': 0, 'high': 0, 'low': 0, None: 0}
        for m in markers:
            status = m.get('status')
            if status in status_counts:
                status_counts[status] += 1
            else:
                status_counts[None] += 1
        
        score = get_health_score(status_counts)
        abnormal = status_counts['high'] + status_counts['low']
        
        categories.append({
            'id': cat,
            'name': category_config[cat]['name'],
            'score': score,
            'status': 'optimal' if score >= 80 else 'attention' if score >= 60 else 'critical',
            'icon': category_config[cat]['icon'],
            'markers_count': len(markers),
            'abnormal_count': abnormal
        })
    
    return sorted(categories, key=lambda x: x['score'])


def generate_recommendations(user_id: str) -> List[Dict[str, Any]]:
    """Generate recommendations based on abnormal biomarkers."""
    biomarkers = user_db_service.get_user_biomarkers(user_id)
    recommendations = []
    rec_id = 1
    
    for b in biomarkers:
        if b['status'] == 'low':
            if b['name'] == 'vitamin_d':
                recommendations.append({
                    'id': rec_id,
                    'title': 'Take Vitamin D3 2000-4000 IU daily',
                    'category': 'nutrition',
                    'priority': 'high',
                    'reason': f"Your Vitamin D is {b['value']} {b['unit']} (deficient)"
                })
            elif b['name'] == 'vitamin_b12':
                recommendations.append({
                    'id': rec_id,
                    'title': 'Take Vitamin B12 1000mcg daily',
                    'category': 'nutrition',
                    'priority': 'high',
                    'reason': f"Your B12 is {b['value']} {b['unit']} (low)"
                })
            elif b['name'] == 'hdl':
                recommendations.append({
                    'id': rec_id,
                    'title': 'Increase HDL with exercise and omega-3',
                    'category': 'lifestyle',
                    'priority': 'medium',
                    'reason': f"Your HDL is {b['value']} {b['unit']} (low)"
                })
            rec_id += 1
        
        elif b['status'] == 'high':
            if b['name'] == 'triglycerides':
                recommendations.append({
                    'id': rec_id,
                    'title': 'Reduce triglycerides with diet and exercise',
                    'category': 'lifestyle',
                    'priority': 'high',
                    'reason': f"Your triglycerides are {b['value']} {b['unit']} (high)"
                })
            elif b['name'] == 'ldl':
                recommendations.append({
                    'id': rec_id,
                    'title': 'Lower LDL with fiber and plant sterols',
                    'category': 'nutrition',
                    'priority': 'medium',
                    'reason': f"Your LDL is {b['value']} {b['unit']} (elevated)"
                })
            rec_id += 1
    
    return recommendations[:6]  # Top 6 recommendations


def generate_health_status(user_id: str) -> Dict[str, Any]:
    """Generate complete health status for a user."""
    user = user_db_service.get_user(user_id)
    if not user:
        return None
    
    categories = generate_health_categories(user_id)
    biomarkers = user_db_service.get_user_biomarkers(user_id)
    
    # Calculate overall score
    if categories:
        overall_score = int(sum(c['score'] for c in categories) / len(categories))
    else:
        overall_score = 0
    
    # Calculate biological age
    bio_age = calculate_bio_age(user['age'], biomarkers)
    
    # Generate insights
    insights = generate_insights(biomarkers, user['age'], bio_age)
    
    return {
        'overall_score': overall_score,
        'age': user['age'],
        'biological_age': bio_age,
        'longevity_score': max(0, 100 - abs(bio_age - user['age']) * 5),
        'categories': categories,
        'key_insights': insights,
        'last_updated': '2024-07-26T12:00:00Z'
    }


def calculate_bio_age(age: int, biomarkers: List[Dict]) -> float:
    """Calculate biological age from biomarkers."""
    adjustment = 0
    
    for b in biomarkers:
        if b['status'] == 'high':
            if b['name'] in ['triglycerides', 'ldl']:
                adjustment += 1.5
        elif b['status'] == 'low':
            if b['name'] == 'hdl':
                adjustment += 2
            elif b['name'] in ['vitamin_d', 'vitamin_b12']:
                adjustment += 1
    
    return round(age + adjustment, 1)


def generate_insights(biomarkers: List[Dict], age: int, bio_age: float) -> List[str]:
    """Generate key insights from biomarkers."""
    insights = []
    
    age_diff = bio_age - age
    if age_diff <= 0:
        insights.append(f"Your biological age is {abs(age_diff):.0f} years younger than your actual age!")
    else:
        insights.append(f"Your biological age is {age_diff:.0f} years older - room for improvement")
    
    for b in biomarkers:
        if b['status'] == 'low' and b['name'] == 'vitamin_d':
            insights.append(f"Vitamin D deficiency ({b['value']} {b['unit']}) needs attention")
        if b['status'] == 'high' and b['name'] == 'triglycerides':
            insights.append(f"High triglycerides ({b['value']} {b['unit']}) - consider diet changes")
        if b['status'] == 'low' and b['name'] == 'hdl':
            insights.append(f"Low HDL ({b['value']} {b['unit']}) - increase cardio exercise")
    
    if len(insights) < 3:
        insights.append("Regular monitoring recommended for optimal health")
    
    return insights[:6]


def generate_health_metrics(user_id: str) -> List[Dict[str, Any]]:
    """Generate health metrics summary."""
    biomarkers = user_db_service.get_user_biomarkers_by_category(user_id)
    if not biomarkers:
        return []
    
    metrics = []
    for cat, markers in biomarkers.items():
        for m in markers:
            metrics.append({
                'id': m['name'],
                'name': m['name'].replace('_', ' ').title(),
                'value': m['value'],
                'unit': m['unit'] or '',
                'status': m['status'],
                'category': cat
            })
    
    return metrics[:12]  # Top 12 metrics
