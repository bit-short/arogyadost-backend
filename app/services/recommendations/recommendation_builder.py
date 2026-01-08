from typing import List
from .models import DigitalTwin, Recommendation
from .biomarker_rules import BiomarkerRuleEvaluator
from .condition_rules import ConditionRuleEvaluator
from .demographic_rules import DemographicRuleEvaluator
from .temporal_rules import TemporalRuleEvaluator


class RecommendationBuilder:
    """Builds recommendations by integrating all rule evaluators."""
    
    def __init__(self):
        self.biomarker_evaluator = BiomarkerRuleEvaluator()
        self.condition_evaluator = ConditionRuleEvaluator()
        self.demographic_evaluator = DemographicRuleEvaluator()
        self.temporal_evaluator = TemporalRuleEvaluator()
    
    def build_recommendations(self, twin: DigitalTwin) -> List[Recommendation]:
        """Build comprehensive recommendations from all rule evaluators."""
        all_recommendations = []
        
        # Collect recommendations from all evaluators
        all_recommendations.extend(self.biomarker_evaluator.evaluate(twin))
        all_recommendations.extend(self.condition_evaluator.evaluate(twin))
        all_recommendations.extend(self.demographic_evaluator.evaluate(twin))
        all_recommendations.extend(self.temporal_evaluator.evaluate(twin))
        
        # Deduplicate and merge similar recommendations
        deduplicated = self._deduplicate_recommendations(all_recommendations)
        
        # Ensure all recommendations have required fields
        validated = self._validate_recommendations(deduplicated)
        
        return validated
    
    def _deduplicate_recommendations(self, recommendations: List[Recommendation]) -> List[Recommendation]:
        """Remove duplicate recommendations and merge similar ones."""
        # Group by test name
        test_groups = {}
        for rec in recommendations:
            test_name = rec.test_name.lower().strip()
            if test_name not in test_groups:
                test_groups[test_name] = []
            test_groups[test_name].append(rec)
        
        deduplicated = []
        for test_name, group in test_groups.items():
            if len(group) == 1:
                deduplicated.append(group[0])
            else:
                # Merge multiple recommendations for the same test
                merged = self._merge_recommendations(group)
                deduplicated.append(merged)
        
        return deduplicated
    
    def _merge_recommendations(self, recommendations: List[Recommendation]) -> Recommendation:
        """Merge multiple recommendations for the same test."""
        # Use the first recommendation as base
        base_rec = recommendations[0]
        
        # Combine rationales
        rationales = []
        for rec in recommendations:
            if rec.rationale and rec.rationale not in rationales:
                rationales.append(rec.rationale)
        
        # Use highest priority
        priorities = [rec.priority for rec in recommendations]
        highest_priority = self._get_highest_priority(priorities)
        
        # Combine related biomarkers and conditions
        all_biomarkers = set()
        all_conditions = set()
        
        for rec in recommendations:
            all_biomarkers.update(rec.related_biomarkers)
            all_conditions.update(rec.related_conditions)
        
        # Use most urgent timing
        timings = [rec.suggested_timing for rec in recommendations]
        most_urgent_timing = self._get_most_urgent_timing(timings)
        
        # Create merged recommendation
        merged = Recommendation(
            test_name=base_rec.test_name,
            test_category=base_rec.test_category,
            rationale="; ".join(rationales),
            priority=highest_priority,
            suggested_timing=most_urgent_timing,
            related_biomarkers=list(all_biomarkers),
            related_conditions=list(all_conditions),
            educational_context=base_rec.educational_context or self._generate_educational_context(base_rec)
        )
        
        return merged
    
    def _validate_recommendations(self, recommendations: List[Recommendation]) -> List[Recommendation]:
        """Ensure all recommendations have required fields."""
        validated = []
        
        for rec in recommendations:
            # Ensure rationale is present
            if not rec.rationale:
                rec.rationale = f"Recommended {rec.test_name} based on health assessment"
            
            # Ensure timing is present
            if not rec.suggested_timing:
                rec.suggested_timing = "within 4 weeks"
            
            # Ensure educational context is present
            if not rec.educational_context:
                rec.educational_context = self._generate_educational_context(rec)
            
            validated.append(rec)
        
        return validated
    
    def _get_highest_priority(self, priorities: List[str]) -> str:
        """Get the highest priority from a list."""
        priority_order = {"high": 3, "medium": 2, "low": 1}
        
        highest_score = 0
        highest_priority = "low"
        
        for priority in priorities:
            score = priority_order.get(priority.lower(), 1)
            if score > highest_score:
                highest_score = score
                highest_priority = priority
        
        return highest_priority
    
    def _get_most_urgent_timing(self, timings: List[str]) -> str:
        """Get the most urgent timing from a list."""
        # Simple urgency scoring based on keywords
        urgency_scores = {}
        
        for timing in timings:
            timing_lower = timing.lower()
            if "1 week" in timing_lower or "immediately" in timing_lower:
                urgency_scores[timing] = 7
            elif "2 weeks" in timing_lower:
                urgency_scores[timing] = 6
            elif "1 month" in timing_lower:
                urgency_scores[timing] = 5
            elif "6 weeks" in timing_lower:
                urgency_scores[timing] = 4
            elif "2 months" in timing_lower:
                urgency_scores[timing] = 3
            elif "3 months" in timing_lower:
                urgency_scores[timing] = 2
            else:
                urgency_scores[timing] = 1
        
        # Return timing with highest urgency score
        if urgency_scores:
            return max(urgency_scores.items(), key=lambda x: x[1])[0]
        
        return "within 4 weeks"
    
    def _generate_educational_context(self, recommendation: Recommendation) -> str:
        """Generate educational context for a recommendation."""
        test_name = recommendation.test_name.lower()
        
        educational_contexts = {
            "lipid": "Lipid testing helps assess cardiovascular disease risk and guides treatment decisions",
            "glucose": "Glucose monitoring is essential for diabetes prevention and management",
            "vitamin d": "Vitamin D is crucial for bone health, immune function, and overall wellness",
            "b12": "Vitamin B12 is essential for nerve function, red blood cell formation, and energy metabolism",
            "thyroid": "Thyroid function affects metabolism, energy levels, and overall health",
            "kidney": "Kidney function tests help detect early signs of kidney disease",
            "liver": "Liver function tests assess liver health and detect potential problems early",
            "blood count": "Complete blood count screens for anemia, infections, and blood disorders",
            "metabolic": "Metabolic panels provide a comprehensive view of your body's chemical balance"
        }
        
        for key, context in educational_contexts.items():
            if key in test_name:
                return context
        
        return f"Regular monitoring of {recommendation.test_name} helps maintain optimal health"
