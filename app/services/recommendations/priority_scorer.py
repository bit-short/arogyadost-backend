from typing import List
from .models import DigitalTwin, Recommendation, PriorityLevel


class PriorityScorer:
    """Assigns priority scores and levels to recommendations."""
    
    def assign_priorities(self, recommendations: List[Recommendation], twin: DigitalTwin) -> List[Recommendation]:
        """Assign priority scores and levels to all recommendations."""
        for rec in recommendations:
            rec.priority_score = self.calculate_priority_score(rec, twin)
            rec.priority = self._score_to_priority_level(rec.priority_score)
        
        return recommendations
    
    def calculate_priority_score(self, rec: Recommendation, twin: DigitalTwin) -> float:
        """Calculate priority score for a recommendation."""
        score = 0.0
        
        # Factor 1: Abnormality severity (0.3 weight)
        abnormality_score = self._assess_abnormality_severity(rec, twin)
        score += abnormality_score * 0.3
        
        # Factor 2: Clinical significance (0.25 weight)
        clinical_score = self._assess_clinical_significance(rec, twin)
        score += clinical_score * 0.25
        
        # Factor 3: Time sensitivity (0.2 weight)
        time_score = self._assess_time_sensitivity(rec, twin)
        score += time_score * 0.2
        
        # Factor 4: Risk factor count (0.15 weight)
        risk_score = self._assess_risk_factors(rec, twin)
        score += risk_score * 0.15
        
        # Factor 5: Condition severity (0.1 weight)
        condition_score = self._assess_condition_severity(rec, twin)
        score += condition_score * 0.1
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _assess_abnormality_severity(self, rec: Recommendation, twin: DigitalTwin) -> float:
        """Assess severity of biomarker abnormalities."""
        if not twin.latest_biomarkers or not rec.related_biomarkers:
            return 0.3  # Default moderate score for missing data
        
        max_severity = 0.0
        
        for biomarker in rec.related_biomarkers:
            severity = self._get_biomarker_severity(biomarker, twin)
            max_severity = max(max_severity, severity)
        
        return max_severity
    
    def _get_biomarker_severity(self, biomarker: str, twin: DigitalTwin) -> float:
        """Get severity score for a specific biomarker."""
        if not twin.latest_biomarkers:
            return 0.3
        
        # Search for biomarker in all categories
        for category, markers in twin.latest_biomarkers.categories.items():
            if biomarker in markers:
                marker_value = markers[biomarker]
                if marker_value.status == "high":
                    return 0.8  # High abnormality
                elif marker_value.status == "low":
                    return 0.7  # Low abnormality
                else:
                    return 0.1  # Normal
        
        return 0.3  # Not found, moderate priority
    
    def _assess_clinical_significance(self, rec: Recommendation, twin: DigitalTwin) -> float:
        """Assess clinical significance of the test."""
        test_name = rec.test_name.lower()
        
        # High clinical significance tests
        high_significance = [
            "glucose", "hba1c", "cholesterol", "ldl", "creatinine",
            "liver function", "kidney function", "cardiac"
        ]
        
        # Medium clinical significance tests
        medium_significance = [
            "vitamin d", "b12", "thyroid", "complete blood count",
            "metabolic panel", "lipid profile"
        ]
        
        for high_test in high_significance:
            if high_test in test_name:
                return 0.9
        
        for medium_test in medium_significance:
            if medium_test in test_name:
                return 0.6
        
        return 0.4  # Default moderate significance
    
    def _assess_time_sensitivity(self, rec: Recommendation, twin: DigitalTwin) -> float:
        """Assess time sensitivity based on suggested timing."""
        timing = rec.suggested_timing.lower()
        
        if "immediately" in timing or "1 week" in timing:
            return 1.0
        elif "2 weeks" in timing:
            return 0.8
        elif "1 month" in timing:
            return 0.6
        elif "6 weeks" in timing or "2 months" in timing:
            return 0.4
        elif "3 months" in timing:
            return 0.2
        else:
            return 0.3  # Default
    
    def _assess_risk_factors(self, rec: Recommendation, twin: DigitalTwin) -> float:
        """Assess number of risk factors present."""
        risk_count = 0
        
        # Age-based risk
        if twin.demographics.age >= 65:
            risk_count += 2
        elif twin.demographics.age >= 40:
            risk_count += 1
        
        # Condition-based risk
        high_risk_conditions = [
            "diabetes", "heart disease", "kidney disease", "liver disease",
            "hypertension", "dyslipidemia"
        ]
        
        for condition in twin.conditions:
            if condition.status == "active":
                condition_name = condition.condition.lower()
                if any(hrc in condition_name for hrc in high_risk_conditions):
                    risk_count += 2
                else:
                    risk_count += 1
        
        # Family history risk
        family_conditions = [fh.condition.lower() for fh in twin.family_history]
        high_risk_family = ["heart disease", "diabetes", "cancer"]
        
        for family_condition in family_conditions:
            if any(hrf in family_condition for hrf in high_risk_family):
                risk_count += 1
        
        # Lifestyle risk factors
        if twin.lifestyle:
            if twin.lifestyle.smoking and twin.lifestyle.smoking.get("status") == "current":
                risk_count += 2
            if twin.lifestyle.alcohol and twin.lifestyle.alcohol.get("frequency") == "daily":
                risk_count += 1
            if twin.lifestyle.exercise_frequency in ["never", "rarely"]:
                risk_count += 1
        
        # Convert risk count to score (0-1)
        return min(risk_count / 10.0, 1.0)
    
    def _assess_condition_severity(self, rec: Recommendation, twin: DigitalTwin) -> float:
        """Assess severity of related conditions."""
        if not rec.related_conditions:
            return 0.0
        
        max_severity = 0.0
        
        for condition_name in rec.related_conditions:
            # Find matching condition in twin
            for condition in twin.conditions:
                if condition.condition.lower() == condition_name.lower():
                    severity = self._get_condition_severity_score(condition)
                    max_severity = max(max_severity, severity)
        
        return max_severity
    
    def _get_condition_severity_score(self, condition) -> float:
        """Get severity score for a medical condition."""
        if hasattr(condition, 'severity') and condition.severity:
            severity = condition.severity.lower()
            if severity in ["severe", "critical"]:
                return 1.0
            elif severity in ["moderate"]:
                return 0.6
            elif severity in ["mild"]:
                return 0.3
        
        # Default severity based on condition type
        high_severity_conditions = [
            "diabetes", "heart disease", "kidney disease", "liver disease"
        ]
        
        condition_name = condition.condition.lower()
        if any(hsc in condition_name for hsc in high_severity_conditions):
            return 0.8
        
        return 0.4  # Default moderate severity
    
    def _score_to_priority_level(self, score: float) -> PriorityLevel:
        """Convert priority score to priority level."""
        if score >= 0.7:
            return PriorityLevel.HIGH
        elif score >= 0.4:
            return PriorityLevel.MEDIUM
        else:
            return PriorityLevel.LOW
