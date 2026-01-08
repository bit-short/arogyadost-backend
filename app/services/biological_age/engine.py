from typing import Dict, Any, List
from app.models.digital_twin import DigitalTwin
from .calculator import BiologicalAgeCalculator


class BiologicalAgeEngine:
    """Main engine for biological age prediction using Digital Twin data"""
    
    def __init__(self):
        self.calculator = BiologicalAgeCalculator()
    
    def predict_biological_age(self, digital_twin: DigitalTwin) -> Dict[str, Any]:
        """Predict biological age from a Digital Twin"""
        # Extract user data from digital twin
        age_data = digital_twin.get_value("demographics", "age")
        gender_data = digital_twin.get_value("demographics", "gender")
        
        if not age_data:
            raise ValueError(f"Age data not found in digital twin for {digital_twin.user_id}")
        
        # Get all biomarkers from digital twin
        biomarkers_domain = digital_twin.get_domain("biomarkers")
        biomarkers = {}
        
        if biomarkers_domain:
            for field_name, field in biomarkers_domain.fields.items():
                if field.values:
                    latest = field.get_latest_value()
                    biomarkers[field_name] = {
                        'value': latest.value,
                        'unit': latest.unit,
                        'timestamp': latest.timestamp
                    }
        
        # Prepare data for calculation
        user_data = {
            'age': age_data.value,
            'gender': gender_data.value if gender_data else 'unknown',
            'biomarkers': biomarkers
        }
        
        # Calculate biological age
        result = self.calculator.calculate_biological_age(user_data)
        result['user_id'] = digital_twin.user_id
        
        return result
    
    def get_age_insights(self, digital_twin: DigitalTwin) -> Dict[str, Any]:
        """Get detailed age insights and recommendations from Digital Twin"""
        result = self.predict_biological_age(digital_twin)
        
        insights = {
            'user_id': digital_twin.user_id,
            'biological_age': result['biological_age'],
            'chronological_age': result['chronological_age'],
            'age_delta': result['age_delta'],
            'status': self._get_age_status(result['age_delta']),
            'confidence': result['confidence_score'],
            'category_breakdown': result['category_ages'],
            'recommendations': self._generate_recommendations(result),
            'data_completeness': digital_twin.get_overall_completeness()
        }
        
        return insights
    
    def _get_age_status(self, age_delta: float) -> str:
        """Get age status description"""
        if age_delta <= -5:
            return "Excellent - significantly younger than chronological age"
        elif age_delta <= -2:
            return "Good - younger than chronological age"
        elif age_delta <= 2:
            return "Average - close to chronological age"
        elif age_delta <= 5:
            return "Attention needed - older than chronological age"
        else:
            return "High priority - significantly older than chronological age"
    
    def _generate_recommendations(self, result: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on biological age results"""
        recommendations = []
        category_ages = result['category_ages']
        chronological_age = result['chronological_age']
        
        # Metabolic recommendations
        if category_ages['metabolic'] > chronological_age + 3:
            recommendations.append("Focus on metabolic health: implement intermittent fasting and reduce refined carbs")
        
        # Cardiovascular recommendations
        if category_ages['cardiovascular'] > chronological_age + 3:
            recommendations.append("Improve cardiovascular health: add Zone 2 cardio and omega-3 supplements")
        
        # Hormonal recommendations
        if category_ages['hormonal'] > chronological_age + 3:
            recommendations.append("Optimize hormones: prioritize 7-8 hours sleep and manage stress")
        
        # Organ function recommendations
        if category_ages['organ_function'] > chronological_age + 3:
            recommendations.append("Support organ function: stay hydrated and consider liver/kidney support supplements")
        
        # General recommendations
        if result['age_delta'] > 5:
            recommendations.append("Consider comprehensive lifestyle intervention with medical supervision")
        
        return recommendations
