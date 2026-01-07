from typing import List
from .models import DigitalTwin, Recommendation, TestCategory, PriorityLevel
from datetime import datetime, timedelta


class TemporalRuleEvaluator:
    """Evaluates timing of tests and generates recommendations based on intervals."""
    
    def __init__(self):
        # Standard monitoring intervals for different test types (in months)
        self.standard_intervals = {
            "routine_metabolic": 12,  # Annual
            "routine_lipid": 12,      # Annual
            "routine_cbc": 12,        # Annual
            "routine_vitamins": 12,   # Annual
            "condition_monitoring": 3, # Quarterly for active conditions
            "post_intervention": 2,   # 6-8 weeks after starting treatment
            "abnormal_followup": 1,   # Monthly for abnormal results
        }
    
    def evaluate(self, twin: DigitalTwin) -> List[Recommendation]:
        """Generate temporal-based recommendations."""
        recommendations = []
        
        # Check routine monitoring intervals
        recommendations.extend(self._check_routine_intervals(twin))
        
        # Check post-intervention testing
        recommendations.extend(self._check_post_intervention(twin))
        
        # Check overdue monitoring
        recommendations.extend(self._check_overdue_monitoring(twin))
        
        return recommendations
    
    def _check_routine_intervals(self, twin: DigitalTwin) -> List[Recommendation]:
        """Check if routine monitoring is due."""
        recommendations = []
        
        if not twin.latest_biomarkers:
            # No previous tests - recommend comprehensive baseline
            return self._recommend_baseline_panel(twin)
        
        # Check how long since last comprehensive testing
        time_since_last = datetime.now() - twin.latest_biomarkers.test_date
        
        # Annual routine screening
        if time_since_last.days >= 365:
            recommendations.extend(self._recommend_annual_screening(twin))
        
        # Check specific category intervals
        recommendations.extend(self._check_category_intervals(twin))
        
        return recommendations
    
    def _check_post_intervention(self, twin: DigitalTwin) -> List[Recommendation]:
        """Check for post-intervention testing needs."""
        recommendations = []
        
        # Check recent medication/supplement starts
        cutoff_date = datetime.now() - timedelta(weeks=6)  # 6 weeks ago
        
        recent_medications = [
            med for med in twin.medications 
            if med.start_date and med.start_date >= cutoff_date
        ]
        
        recent_supplements = [
            supp for supp in twin.supplements 
            if supp.start_date and supp.start_date >= cutoff_date
        ]
        
        # Recommend follow-up testing for recent interventions
        for med in recent_medications:
            rec = self._create_post_medication_recommendation(med, twin)
            if rec:
                recommendations.append(rec)
        
        for supp in recent_supplements:
            rec = self._create_post_supplement_recommendation(supp, twin)
            if rec:
                recommendations.append(rec)
        
        return recommendations
    
    def _check_overdue_monitoring(self, twin: DigitalTwin) -> List[Recommendation]:
        """Check for overdue monitoring based on conditions."""
        recommendations = []
        
        active_conditions = [c for c in twin.conditions if c.status == "active"]
        
        for condition in active_conditions:
            if self._is_condition_monitoring_overdue(condition, twin):
                rec = self._create_overdue_monitoring_recommendation(condition, twin)
                if rec:
                    recommendations.append(rec)
        
        return recommendations
    
    def _recommend_baseline_panel(self, twin: DigitalTwin) -> List[Recommendation]:
        """Recommend comprehensive baseline panel for new users."""
        return [
            Recommendation(
                test_name="Comprehensive Health Panel",
                test_category=TestCategory.METABOLIC,
                rationale="Comprehensive baseline health assessment",
                priority=PriorityLevel.MEDIUM,
                suggested_timing="within 2 weeks",
                related_biomarkers=[
                    "glucose", "cholesterol", "ldl", "hdl", "triglycerides",
                    "hemoglobin", "white_blood_cells", "creatinine", "alt", "ast"
                ],
                educational_context="Baseline testing establishes your health profile and identifies areas for optimization"
            ),
            Recommendation(
                test_name="Vitamin and Mineral Panel",
                test_category=TestCategory.VITAMINS,
                rationale="Baseline vitamin and mineral assessment",
                priority=PriorityLevel.MEDIUM,
                suggested_timing="within 2 weeks",
                related_biomarkers=["vitamin_d", "b12", "folate", "iron", "magnesium"],
                educational_context="Vitamin and mineral deficiencies are common and easily correctable"
            )
        ]
    
    def _recommend_annual_screening(self, twin: DigitalTwin) -> List[Recommendation]:
        """Recommend annual routine screening."""
        recommendations = []
        
        # Annual metabolic panel
        recommendations.append(Recommendation(
            test_name="Annual Metabolic Panel",
            test_category=TestCategory.METABOLIC,
            rationale="Annual routine metabolic health screening",
            priority=PriorityLevel.MEDIUM,
            suggested_timing="within 1 month",
            related_biomarkers=["glucose", "creatinine", "electrolytes"],
            educational_context="Annual screening helps detect changes in metabolic health over time"
        ))
        
        # Annual lipid screening
        recommendations.append(Recommendation(
            test_name="Annual Lipid Profile",
            test_category=TestCategory.LIPID_PROFILE,
            rationale="Annual cardiovascular risk assessment",
            priority=PriorityLevel.MEDIUM,
            suggested_timing="within 1 month",
            related_biomarkers=["cholesterol", "ldl", "hdl", "triglycerides"],
            educational_context="Regular lipid monitoring is key to cardiovascular disease prevention"
        ))
        
        return recommendations
    
    def _check_category_intervals(self, twin: DigitalTwin) -> List[Recommendation]:
        """Check intervals for specific biomarker categories."""
        recommendations = []
        
        if not twin.latest_biomarkers:
            return recommendations
        
        # Check which categories are missing or outdated
        time_since_last = datetime.now() - twin.latest_biomarkers.test_date
        existing_categories = set(twin.latest_biomarkers.categories.keys())
        
        # Essential categories that should be tested annually
        essential_categories = {
            "metabolic": ("Metabolic Panel", TestCategory.METABOLIC),
            "lipid_profile": ("Lipid Profile", TestCategory.LIPID_PROFILE),
            "complete_blood_count": ("Complete Blood Count", TestCategory.COMPLETE_BLOOD_COUNT),
            "vitamins": ("Vitamin Panel", TestCategory.VITAMINS)
        }
        
        # If it's been more than a year, recommend missing categories
        if time_since_last.days >= 365:
            for category, (test_name, test_category) in essential_categories.items():
                if category not in existing_categories:
                    recommendations.append(Recommendation(
                        test_name=test_name,
                        test_category=test_category,
                        rationale=f"Missing {category.replace('_', ' ')} data from recent testing",
                        priority=PriorityLevel.MEDIUM,
                        suggested_timing="within 6 weeks",
                        educational_context=f"Regular {category.replace('_', ' ')} monitoring is important for comprehensive health assessment"
                    ))
        
        return recommendations
    
    def _create_post_medication_recommendation(self, medication, twin: DigitalTwin) -> Recommendation:
        """Create post-medication monitoring recommendation."""
        # Map common medications to monitoring tests
        med_monitoring = {
            "statin": ("Liver Function Panel", TestCategory.LIVER_FUNCTION, ["alt", "ast"]),
            "metformin": ("Metabolic Panel", TestCategory.METABOLIC, ["glucose", "hba1c"]),
            "ace_inhibitor": ("Kidney Function", TestCategory.KIDNEY_FUNCTION, ["creatinine", "potassium"]),
            "diuretic": ("Electrolyte Panel", TestCategory.METABOLIC, ["sodium", "potassium"])
        }
        
        med_name = medication.name.lower()
        for med_type, (test_name, category, biomarkers) in med_monitoring.items():
            if med_type in med_name:
                return Recommendation(
                    test_name=test_name,
                    test_category=category,
                    rationale=f"Post-medication monitoring for {medication.name}",
                    priority=PriorityLevel.MEDIUM,
                    suggested_timing="within 2 weeks",
                    related_biomarkers=biomarkers,
                    educational_context=f"Monitoring after starting {medication.name} ensures safety and effectiveness"
                )
        
        # Generic post-medication monitoring
        return Recommendation(
            test_name="Post-Medication Monitoring",
            test_category=TestCategory.METABOLIC,
            rationale=f"Safety monitoring after starting {medication.name}",
            priority=PriorityLevel.MEDIUM,
            suggested_timing="within 4 weeks",
            educational_context="Regular monitoring after starting new medications helps ensure safety"
        )
    
    def _create_post_supplement_recommendation(self, supplement, twin: DigitalTwin) -> Recommendation:
        """Create post-supplement monitoring recommendation."""
        supp_name = supplement.name.lower()
        
        if "vitamin d" in supp_name:
            return Recommendation(
                test_name="Vitamin D",
                test_category=TestCategory.VITAMINS,
                rationale="Monitor vitamin D levels after supplementation",
                priority=PriorityLevel.LOW,
                suggested_timing="within 8 weeks",
                related_biomarkers=["vitamin_d"],
                educational_context="Vitamin D levels should be rechecked 6-8 weeks after starting supplementation"
            )
        elif "b12" in supp_name:
            return Recommendation(
                test_name="Vitamin B12",
                test_category=TestCategory.VITAMINS,
                rationale="Monitor B12 levels after supplementation",
                priority=PriorityLevel.LOW,
                suggested_timing="within 8 weeks",
                related_biomarkers=["b12"],
                educational_context="B12 levels should be rechecked after supplementation to ensure adequacy"
            )
        
        return None
    
    def _is_condition_monitoring_overdue(self, condition, twin: DigitalTwin) -> bool:
        """Check if condition monitoring is overdue."""
        if not twin.latest_biomarkers:
            return True
        
        # High-priority conditions need more frequent monitoring
        high_priority_conditions = ["diabetes", "kidney_disease", "liver_disease"]
        condition_name = condition.condition.lower()
        
        monitoring_interval = 3  # Default 3 months
        if any(hpc in condition_name for hpc in high_priority_conditions):
            monitoring_interval = 2  # 2 months for high-priority conditions
        
        cutoff_date = datetime.now() - timedelta(days=monitoring_interval * 30)
        return twin.latest_biomarkers.test_date < cutoff_date
    
    def _create_overdue_monitoring_recommendation(self, condition, twin: DigitalTwin) -> Recommendation:
        """Create overdue monitoring recommendation."""
        return Recommendation(
            test_name=f"{condition.condition} Monitoring Panel",
            test_category=TestCategory.METABOLIC,
            rationale=f"Overdue monitoring for {condition.condition}",
            priority=PriorityLevel.HIGH,
            suggested_timing="within 1 week",
            related_conditions=[condition.condition],
            educational_context=f"Regular monitoring of {condition.condition} is critical for proper management"
        )
