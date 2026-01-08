from typing import List, Dict
from .models import DigitalTwin, Recommendation, TestCategory, PriorityLevel


class ConditionRuleEvaluator:
    """Evaluates medical conditions and generates monitoring recommendations."""
    
    def __init__(self):
        # Mapping of conditions to required monitoring tests
        self.condition_monitoring_map = {
            "dyslipidemia": {
                "tests": ["Lipid Profile"],
                "category": TestCategory.LIPID_PROFILE,
                "frequency_months": 3,
                "biomarkers": ["cholesterol", "ldl", "hdl", "triglycerides"]
            },
            "vitamin_d_deficiency": {
                "tests": ["Vitamin D"],
                "category": TestCategory.VITAMINS,
                "frequency_months": 3,
                "biomarkers": ["vitamin_d"]
            },
            "diabetes": {
                "tests": ["HbA1c", "Fasting Glucose"],
                "category": TestCategory.METABOLIC,
                "frequency_months": 3,
                "biomarkers": ["hba1c", "glucose"]
            },
            "prediabetes": {
                "tests": ["HbA1c", "Fasting Glucose"],
                "category": TestCategory.METABOLIC,
                "frequency_months": 6,
                "biomarkers": ["hba1c", "glucose"]
            },
            "hypertension": {
                "tests": ["Comprehensive Metabolic Panel"],
                "category": TestCategory.METABOLIC,
                "frequency_months": 6,
                "biomarkers": ["sodium", "potassium", "creatinine"]
            },
            "kidney_disease": {
                "tests": ["Kidney Function Panel"],
                "category": TestCategory.KIDNEY_FUNCTION,
                "frequency_months": 3,
                "biomarkers": ["creatinine", "bun", "egfr"]
            },
            "liver_disease": {
                "tests": ["Liver Function Panel"],
                "category": TestCategory.LIVER_FUNCTION,
                "frequency_months": 3,
                "biomarkers": ["alt", "ast", "bilirubin"]
            },
            "anemia": {
                "tests": ["Complete Blood Count", "Iron Studies"],
                "category": TestCategory.COMPLETE_BLOOD_COUNT,
                "frequency_months": 3,
                "biomarkers": ["hemoglobin", "hematocrit", "iron", "ferritin"]
            },
            "thyroid_disorder": {
                "tests": ["Thyroid Function Panel"],
                "category": TestCategory.HORMONES,
                "frequency_months": 6,
                "biomarkers": ["tsh", "t3", "t4"]
            },
            "osteoporosis": {
                "tests": ["Vitamin D", "Calcium"],
                "category": TestCategory.MINERALS,
                "frequency_months": 6,
                "biomarkers": ["vitamin_d", "calcium"]
            }
        }
    
    def evaluate(self, twin: DigitalTwin) -> List[Recommendation]:
        """Generate condition-based monitoring recommendations."""
        recommendations = []
        
        active_conditions = [c for c in twin.conditions if c.status == "active"]
        
        for condition in active_conditions:
            condition_recs = self._create_condition_monitoring(condition, twin)
            recommendations.extend(condition_recs)
        
        return recommendations
    
    def _create_condition_monitoring(self, condition, twin: DigitalTwin) -> List[Recommendation]:
        """Create monitoring recommendations for a specific condition."""
        recommendations = []
        condition_name = condition.condition.lower()
        
        # Find matching condition in our mapping
        monitoring_info = None
        for key, info in self.condition_monitoring_map.items():
            if key in condition_name or condition_name in key:
                monitoring_info = info
                break
        
        if not monitoring_info:
            # Generic monitoring for unknown conditions
            return self._create_generic_monitoring(condition, twin)
        
        # Check if monitoring is due
        if self._is_monitoring_due(twin, monitoring_info):
            for test_name in monitoring_info["tests"]:
                rec = Recommendation(
                    test_name=test_name,
                    test_category=monitoring_info["category"],
                    rationale=f"Routine monitoring for {condition.condition}",
                    priority=self._determine_condition_priority(condition),
                    suggested_timing=self._calculate_monitoring_timing(monitoring_info),
                    related_biomarkers=monitoring_info["biomarkers"],
                    related_conditions=[condition.condition],
                    educational_context=f"Regular monitoring is essential for managing {condition.condition} and preventing complications"
                )
                recommendations.append(rec)
        
        return recommendations
    
    def _create_generic_monitoring(self, condition, twin: DigitalTwin) -> List[Recommendation]:
        """Create generic monitoring for conditions not in our mapping."""
        return [Recommendation(
            test_name="Comprehensive Metabolic Panel",
            test_category=TestCategory.METABOLIC,
            rationale=f"General health monitoring for {condition.condition}",
            priority=PriorityLevel.MEDIUM,
            suggested_timing="within 3 months",
            related_conditions=[condition.condition],
            educational_context=f"Regular health monitoring helps track the impact of {condition.condition} on overall health"
        )]
    
    def _is_monitoring_due(self, twin: DigitalTwin, monitoring_info: Dict) -> bool:
        """Check if monitoring is due based on last test date."""
        if not twin.latest_biomarkers:
            return True  # No recent tests, monitoring is due
        
        # Check if any of the required biomarkers were tested recently
        frequency_months = monitoring_info["frequency_months"]
        required_biomarkers = monitoring_info["biomarkers"]
        
        from datetime import datetime, timedelta
        cutoff_date = datetime.now() - timedelta(days=frequency_months * 30)
        
        # If latest test is older than frequency requirement, monitoring is due
        if twin.latest_biomarkers.test_date < cutoff_date:
            return True
        
        # Check if specific biomarkers were tested
        latest_markers = set()
        for category, markers in twin.latest_biomarkers.categories.items():
            latest_markers.update(markers.keys())
        
        # If any required biomarker is missing from latest test, monitoring is due
        for biomarker in required_biomarkers:
            if biomarker not in latest_markers:
                return True
        
        return False
    
    def _determine_condition_priority(self, condition) -> PriorityLevel:
        """Determine priority based on condition severity and type."""
        high_priority_conditions = [
            "diabetes", "kidney_disease", "liver_disease", "heart_disease"
        ]
        
        condition_name = condition.condition.lower()
        
        # Check severity
        if hasattr(condition, 'severity') and condition.severity:
            if condition.severity.lower() in ["severe", "critical"]:
                return PriorityLevel.HIGH
        
        # Check condition type
        for high_priority in high_priority_conditions:
            if high_priority in condition_name:
                return PriorityLevel.HIGH
        
        return PriorityLevel.MEDIUM
    
    def _calculate_monitoring_timing(self, monitoring_info: Dict) -> str:
        """Calculate appropriate timing for monitoring."""
        frequency_months = monitoring_info["frequency_months"]
        
        if frequency_months <= 1:
            return "within 2 weeks"
        elif frequency_months <= 3:
            return "within 1 month"
        elif frequency_months <= 6:
            return "within 6 weeks"
        else:
            return "within 3 months"
