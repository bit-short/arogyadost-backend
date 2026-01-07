from datetime import datetime, timedelta
from typing import List
from .models import DigitalTwin, Recommendation, TestCategory, PriorityLevel


class BiomarkerRuleEvaluator:
    """Evaluates biomarker data and generates recommendations."""
    
    def evaluate(self, twin: DigitalTwin) -> List[Recommendation]:
        """Generate biomarker-based recommendations."""
        recommendations = []
        
        # Check for missing baseline data
        recommendations.extend(self._check_missing_baseline(twin))
        
        # Check for out-of-range follow-ups
        recommendations.extend(self._check_out_of_range_followup(twin))
        
        # Check for trend monitoring
        recommendations.extend(self._check_trend_monitoring(twin))
        
        return recommendations
    
    def _check_missing_baseline(self, twin: DigitalTwin) -> List[Recommendation]:
        """Recommend baseline testing for missing biomarkers."""
        recommendations = []
        
        if not twin.latest_biomarkers:
            # No biomarker data at all - recommend comprehensive baseline
            return self._comprehensive_baseline_panel(twin)
        
        # Check for missing categories
        existing_categories = set(twin.latest_biomarkers.categories.keys())
        essential_categories = {
            "metabolic", "lipid_profile", "complete_blood_count", 
            "kidney_function", "liver_function", "vitamins"
        }
        
        missing_categories = essential_categories - existing_categories
        
        for category in missing_categories:
            rec = self._create_baseline_recommendation(category, twin)
            if rec:
                recommendations.append(rec)
        
        return recommendations
    
    def _check_out_of_range_followup(self, twin: DigitalTwin) -> List[Recommendation]:
        """Recommend follow-up for abnormal biomarkers."""
        recommendations = []
        
        if not twin.latest_biomarkers:
            return recommendations
        
        for category, markers in twin.latest_biomarkers.categories.items():
            for marker_name, marker_value in markers.items():
                if marker_value.status in ["high", "low"]:
                    rec = self._create_followup_recommendation(
                        marker_name, marker_value, category, twin
                    )
                    recommendations.append(rec)
        
        return recommendations
    
    def _check_trend_monitoring(self, twin: DigitalTwin) -> List[Recommendation]:
        """Recommend monitoring for concerning trends."""
        recommendations = []
        
        if not twin.latest_biomarkers or len(twin.biomarker_history) < 2:
            return recommendations
        
        # Check trends for key biomarkers
        key_markers = [
            "glucose", "cholesterol", "ldl", "hdl", "triglycerides",
            "hba1c", "vitamin_d", "b12", "creatinine"
        ]
        
        for marker in key_markers:
            history = self._get_marker_history(twin, marker)
            if len(history) >= 2 and self._has_concerning_trend(history):
                rec = self._create_trend_monitoring_recommendation(marker, twin)
                if rec:
                    recommendations.append(rec)
        
        return recommendations
    
    def _comprehensive_baseline_panel(self, twin: DigitalTwin) -> List[Recommendation]:
        """Create comprehensive baseline panel recommendations."""
        recommendations = []
        
        # Metabolic panel
        recommendations.append(Recommendation(
            test_name="Comprehensive Metabolic Panel",
            test_category=TestCategory.METABOLIC,
            rationale="Baseline metabolic assessment including glucose, electrolytes, and kidney function",
            priority=PriorityLevel.MEDIUM,
            suggested_timing="within 2 weeks",
            related_biomarkers=["glucose", "sodium", "potassium", "creatinine", "bun"],
            educational_context="Essential baseline tests to assess overall metabolic health and organ function"
        ))
        
        # Lipid profile
        recommendations.append(Recommendation(
            test_name="Lipid Profile",
            test_category=TestCategory.LIPID_PROFILE,
            rationale="Baseline cardiovascular risk assessment",
            priority=PriorityLevel.MEDIUM,
            suggested_timing="within 2 weeks",
            related_biomarkers=["cholesterol", "ldl", "hdl", "triglycerides"],
            educational_context="Evaluates cardiovascular disease risk and guides preventive interventions"
        ))
        
        # Complete blood count
        recommendations.append(Recommendation(
            test_name="Complete Blood Count",
            test_category=TestCategory.COMPLETE_BLOOD_COUNT,
            rationale="Baseline blood cell assessment",
            priority=PriorityLevel.MEDIUM,
            suggested_timing="within 2 weeks",
            related_biomarkers=["hemoglobin", "hematocrit", "white_blood_cells", "platelets"],
            educational_context="Screens for anemia, infections, and blood disorders"
        ))
        
        # Vitamin panel
        recommendations.append(Recommendation(
            test_name="Vitamin D and B12",
            test_category=TestCategory.VITAMINS,
            rationale="Common vitamin deficiencies screening",
            priority=PriorityLevel.MEDIUM,
            suggested_timing="within 4 weeks",
            related_biomarkers=["vitamin_d", "b12"],
            educational_context="Vitamin D and B12 deficiencies are common and easily treatable"
        ))
        
        return recommendations
    
    def _create_baseline_recommendation(self, category: str, twin: DigitalTwin) -> Recommendation:
        """Create recommendation for missing category."""
        category_map = {
            "metabolic": ("Comprehensive Metabolic Panel", TestCategory.METABOLIC, 
                         ["glucose", "sodium", "potassium", "creatinine"]),
            "lipid_profile": ("Lipid Profile", TestCategory.LIPID_PROFILE,
                            ["cholesterol", "ldl", "hdl", "triglycerides"]),
            "complete_blood_count": ("Complete Blood Count", TestCategory.COMPLETE_BLOOD_COUNT,
                                   ["hemoglobin", "hematocrit", "white_blood_cells"]),
            "kidney_function": ("Kidney Function Panel", TestCategory.KIDNEY_FUNCTION,
                              ["creatinine", "bun", "egfr"]),
            "liver_function": ("Liver Function Panel", TestCategory.LIVER_FUNCTION,
                             ["alt", "ast", "bilirubin"]),
            "vitamins": ("Vitamin Panel", TestCategory.VITAMINS,
                        ["vitamin_d", "b12", "folate"])
        }
        
        if category not in category_map:
            return None
        
        test_name, test_category, markers = category_map[category]
        
        return Recommendation(
            test_name=test_name,
            test_category=test_category,
            rationale=f"Missing baseline {category.replace('_', ' ')} data",
            priority=PriorityLevel.MEDIUM,
            suggested_timing="within 4 weeks",
            related_biomarkers=markers,
            educational_context=f"Establishes baseline values for {category.replace('_', ' ')} monitoring"
        )
    
    def _create_followup_recommendation(self, marker_name: str, marker_value, category: str, twin: DigitalTwin) -> Recommendation:
        """Create follow-up recommendation for abnormal biomarker."""
        severity = self._assess_abnormality_severity(marker_value)
        
        if severity == "high":
            priority = PriorityLevel.HIGH
            timing = "within 1 week"
        elif severity == "moderate":
            priority = PriorityLevel.MEDIUM
            timing = "within 4 weeks"
        else:
            priority = PriorityLevel.LOW
            timing = "within 8 weeks"
        
        return Recommendation(
            test_name=f"{marker_name.replace('_', ' ').title()} Retest",
            test_category=TestCategory(category) if category in TestCategory.__members__.values() else TestCategory.METABOLIC,
            rationale=f"{marker_name.replace('_', ' ').title()} is {marker_value.status} ({marker_value.value} {marker_value.unit})",
            priority=priority,
            suggested_timing=timing,
            related_biomarkers=[marker_name],
            educational_context=f"Follow-up testing to monitor {marker_name.replace('_', ' ')} levels and assess treatment response"
        )
    
    def _create_trend_monitoring_recommendation(self, marker: str, twin: DigitalTwin) -> Recommendation:
        """Create recommendation for trend monitoring."""
        return Recommendation(
            test_name=f"{marker.replace('_', ' ').title()} Monitoring",
            test_category=TestCategory.METABOLIC,
            rationale=f"Concerning trend detected in {marker.replace('_', ' ')} levels",
            priority=PriorityLevel.MEDIUM,
            suggested_timing="within 6 weeks",
            related_biomarkers=[marker],
            educational_context=f"Regular monitoring to track {marker.replace('_', ' ')} progression and intervention effectiveness"
        )
    
    def _get_marker_history(self, twin: DigitalTwin, marker: str) -> List[dict]:
        """Get historical values for a marker."""
        history = []
        for snapshot in twin.biomarker_history:
            for category, markers in snapshot.categories.items():
                if marker in markers:
                    history.append({
                        "date": snapshot.test_date,
                        "value": markers[marker].value
                    })
        return sorted(history, key=lambda x: x["date"])
    
    def _has_concerning_trend(self, history: List[dict]) -> bool:
        """Check if biomarker trend is concerning."""
        if len(history) < 2:
            return False
        
        # Simple trend analysis - check if consistently increasing/decreasing
        values = [h["value"] for h in history[-3:]]  # Last 3 values
        
        if len(values) >= 2:
            # Check for consistent upward trend (could indicate worsening)
            increasing = all(values[i] < values[i+1] for i in range(len(values)-1))
            # Check for significant change (>20% from first to last)
            significant_change = abs(values[-1] - values[0]) / values[0] > 0.2
            
            return increasing and significant_change
        
        return False
    
    def _assess_abnormality_severity(self, marker_value) -> str:
        """Assess severity of abnormal biomarker value."""
        # This is a simplified assessment - in practice would use clinical ranges
        if marker_value.status in ["high", "low"]:
            # Could implement more sophisticated severity assessment based on
            # how far outside normal range the value is
            return "moderate"
        return "low"
