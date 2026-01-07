from typing import List
from .models import DigitalTwin, Recommendation, TestCategory, PriorityLevel


class DemographicRuleEvaluator:
    """Evaluates demographics for age and sex-based screening recommendations."""
    
    def evaluate(self, twin: DigitalTwin) -> List[Recommendation]:
        """Generate demographic-based screening recommendations."""
        recommendations = []
        
        # Age-based screening
        recommendations.extend(self._age_based_screening(twin))
        
        # Sex-specific screening
        recommendations.extend(self._sex_specific_screening(twin))
        
        # Family history-based screening
        recommendations.extend(self._family_history_screening(twin))
        
        return recommendations
    
    def _age_based_screening(self, twin: DigitalTwin) -> List[Recommendation]:
        """Generate age-based preventive screening recommendations."""
        recommendations = []
        age = twin.demographics.age
        
        # Adults 18-39: Basic screening
        if 18 <= age <= 39:
            recommendations.extend(self._young_adult_screening(twin))
        
        # Adults 40-64: Enhanced screening
        elif 40 <= age <= 64:
            recommendations.extend(self._middle_age_screening(twin))
        
        # Adults 65+: Senior screening
        elif age >= 65:
            recommendations.extend(self._senior_screening(twin))
        
        return recommendations
    
    def _young_adult_screening(self, twin: DigitalTwin) -> List[Recommendation]:
        """Screening for adults 18-39."""
        recommendations = []
        
        # Basic metabolic screening every 3 years
        if self._is_screening_due(twin, "metabolic", 36):  # 3 years
            recommendations.append(Recommendation(
                test_name="Basic Metabolic Panel",
                test_category=TestCategory.METABOLIC,
                rationale="Routine metabolic screening for young adults",
                priority=PriorityLevel.LOW,
                suggested_timing="within 3 months",
                related_biomarkers=["glucose", "cholesterol"],
                educational_context="Early detection of metabolic issues helps prevent future complications"
            ))
        
        return recommendations
    
    def _middle_age_screening(self, twin: DigitalTwin) -> List[Recommendation]:
        """Screening for adults 40-64."""
        recommendations = []
        
        # Annual lipid screening
        if self._is_screening_due(twin, "lipid", 12):
            recommendations.append(Recommendation(
                test_name="Lipid Profile",
                test_category=TestCategory.LIPID_PROFILE,
                rationale="Annual cardiovascular screening for adults 40+",
                priority=PriorityLevel.MEDIUM,
                suggested_timing="within 2 months",
                related_biomarkers=["cholesterol", "ldl", "hdl", "triglycerides"],
                educational_context="Cardiovascular disease risk increases with age, making regular screening essential"
            ))
        
        # Diabetes screening every 3 years
        if self._is_screening_due(twin, "diabetes", 36):
            recommendations.append(Recommendation(
                test_name="Diabetes Screening",
                test_category=TestCategory.METABOLIC,
                rationale="Routine diabetes screening for adults 40+",
                priority=PriorityLevel.MEDIUM,
                suggested_timing="within 2 months",
                related_biomarkers=["glucose", "hba1c"],
                educational_context="Type 2 diabetes risk increases significantly after age 40"
            ))
        
        return recommendations
    
    def _senior_screening(self, twin: DigitalTwin) -> List[Recommendation]:
        """Screening for adults 65+."""
        recommendations = []
        
        # Annual comprehensive screening
        if self._is_screening_due(twin, "comprehensive", 12):
            recommendations.append(Recommendation(
                test_name="Senior Health Panel",
                test_category=TestCategory.METABOLIC,
                rationale="Comprehensive annual screening for seniors",
                priority=PriorityLevel.MEDIUM,
                suggested_timing="within 1 month",
                related_biomarkers=["glucose", "cholesterol", "kidney_function", "liver_function"],
                educational_context="Comprehensive screening helps detect age-related health changes early"
            ))
        
        # Vitamin D screening (common deficiency in seniors)
        if self._is_screening_due(twin, "vitamin_d", 12):
            recommendations.append(Recommendation(
                test_name="Vitamin D",
                test_category=TestCategory.VITAMINS,
                rationale="Vitamin D screening for bone health in seniors",
                priority=PriorityLevel.MEDIUM,
                suggested_timing="within 6 weeks",
                related_biomarkers=["vitamin_d"],
                educational_context="Vitamin D deficiency is common in seniors and affects bone health"
            ))
        
        return recommendations
    
    def _sex_specific_screening(self, twin: DigitalTwin) -> List[Recommendation]:
        """Generate sex-specific screening recommendations."""
        recommendations = []
        sex = twin.demographics.sex.lower()
        age = twin.demographics.age
        
        if sex == "female":
            recommendations.extend(self._female_specific_screening(twin, age))
        elif sex == "male":
            recommendations.extend(self._male_specific_screening(twin, age))
        
        return recommendations
    
    def _female_specific_screening(self, twin: DigitalTwin, age: int) -> List[Recommendation]:
        """Female-specific screening recommendations."""
        recommendations = []
        
        # Reproductive age hormone screening
        if 18 <= age <= 50:
            if self._is_screening_due(twin, "female_hormones", 24):  # Every 2 years
                recommendations.append(Recommendation(
                    test_name="Female Hormone Panel",
                    test_category=TestCategory.HORMONES,
                    rationale="Reproductive health screening for women",
                    priority=PriorityLevel.LOW,
                    suggested_timing="within 3 months",
                    related_biomarkers=["estrogen", "progesterone", "fsh", "lh"],
                    educational_context="Hormone screening helps assess reproductive health and detect imbalances"
                ))
        
        # Menopause screening
        elif age > 45:
            if self._is_screening_due(twin, "menopause", 12):
                recommendations.append(Recommendation(
                    test_name="Menopause Panel",
                    test_category=TestCategory.HORMONES,
                    rationale="Menopause-related hormone assessment",
                    priority=PriorityLevel.LOW,
                    suggested_timing="within 2 months",
                    related_biomarkers=["fsh", "estrogen"],
                    educational_context="Hormone changes during menopause affect bone health and cardiovascular risk"
                ))
        
        return recommendations
    
    def _male_specific_screening(self, twin: DigitalTwin, age: int) -> List[Recommendation]:
        """Male-specific screening recommendations."""
        recommendations = []
        
        # Testosterone screening for men 30+
        if age >= 30:
            if self._is_screening_due(twin, "testosterone", 24):  # Every 2 years
                recommendations.append(Recommendation(
                    test_name="Testosterone",
                    test_category=TestCategory.HORMONES,
                    rationale="Testosterone screening for men 30+",
                    priority=PriorityLevel.LOW,
                    suggested_timing="within 3 months",
                    related_biomarkers=["testosterone"],
                    educational_context="Testosterone levels naturally decline with age, affecting energy and health"
                ))
        
        # PSA screening for men 50+
        if age >= 50:
            if self._is_screening_due(twin, "psa", 12):
                recommendations.append(Recommendation(
                    test_name="PSA (Prostate-Specific Antigen)",
                    test_category=TestCategory.TUMOR_MARKERS,
                    rationale="Prostate cancer screening for men 50+",
                    priority=PriorityLevel.MEDIUM,
                    suggested_timing="within 2 months",
                    related_biomarkers=["psa"],
                    educational_context="PSA screening helps detect prostate cancer early when treatment is most effective"
                ))
        
        return recommendations
    
    def _family_history_screening(self, twin: DigitalTwin) -> List[Recommendation]:
        """Generate screening based on family history."""
        recommendations = []
        
        family_conditions = [fh.condition.lower() for fh in twin.family_history]
        
        # Enhanced cardiovascular screening for family history
        if any("heart" in condition or "cardiovascular" in condition for condition in family_conditions):
            if self._is_screening_due(twin, "enhanced_cardiac", 6):  # Every 6 months
                recommendations.append(Recommendation(
                    test_name="Enhanced Cardiac Panel",
                    test_category=TestCategory.CARDIOVASCULAR,
                    rationale="Enhanced screening due to family history of heart disease",
                    priority=PriorityLevel.MEDIUM,
                    suggested_timing="within 6 weeks",
                    related_biomarkers=["cholesterol", "ldl", "hdl", "triglycerides", "crp"],
                    educational_context="Family history of heart disease increases your risk, making regular screening important"
                ))
        
        # Enhanced diabetes screening for family history
        if any("diabetes" in condition for condition in family_conditions):
            if self._is_screening_due(twin, "enhanced_diabetes", 12):
                recommendations.append(Recommendation(
                    test_name="Enhanced Diabetes Screening",
                    test_category=TestCategory.METABOLIC,
                    rationale="Enhanced screening due to family history of diabetes",
                    priority=PriorityLevel.MEDIUM,
                    suggested_timing="within 1 month",
                    related_biomarkers=["glucose", "hba1c", "insulin"],
                    educational_context="Family history of diabetes significantly increases your risk of developing the condition"
                ))
        
        return recommendations
    
    def _is_screening_due(self, twin: DigitalTwin, screening_type: str, months_interval: int) -> bool:
        """Check if a specific type of screening is due."""
        if not twin.latest_biomarkers:
            return True  # No recent tests, screening is due
        
        from datetime import datetime, timedelta
        cutoff_date = datetime.now() - timedelta(days=months_interval * 30)
        
        # If latest test is older than interval, screening is due
        return twin.latest_biomarkers.test_date < cutoff_date
