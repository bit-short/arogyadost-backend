from typing import List, Dict
from .models import Recommendation, RecommendationResponse, RecommendationSummary, TestCategory
from datetime import datetime


class OutputFormatter:
    """Formats recommendations into structured API response."""
    
    def format_recommendations(self, recommendations: List[Recommendation], user_id: str) -> RecommendationResponse:
        """Format recommendations into API response structure."""
        # Sort recommendations by priority score (highest first)
        sorted_recommendations = sorted(
            recommendations, 
            key=lambda x: (self._priority_to_score(x.priority), x.priority_score), 
            reverse=True
        )
        
        # Add educational context to all recommendations
        enhanced_recommendations = [
            self.add_educational_context(rec) for rec in sorted_recommendations
        ]
        
        # Group by category
        grouped = self.group_by_category(enhanced_recommendations)
        
        # Generate summary
        summary = self._generate_summary(enhanced_recommendations)
        
        return RecommendationResponse(
            user_id=user_id,
            generated_at=datetime.now(),
            summary=summary,
            recommendations=enhanced_recommendations,
            grouped_by_category=grouped
        )
    
    def group_by_category(self, recommendations: List[Recommendation]) -> Dict[str, List[Recommendation]]:
        """Group recommendations by test category."""
        grouped = {}
        
        for rec in recommendations:
            category = rec.test_category.value
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(rec)
        
        # Sort within each category by priority
        for category in grouped:
            grouped[category].sort(
                key=lambda x: (self._priority_to_score(x.priority), x.priority_score),
                reverse=True
            )
        
        return grouped
    
    def add_educational_context(self, recommendation: Recommendation) -> Recommendation:
        """Add or enhance educational context for a recommendation."""
        if recommendation.educational_context:
            return recommendation  # Already has context
        
        # Generate educational context based on test name and category
        context = self._generate_educational_context(recommendation)
        recommendation.educational_context = context
        
        return recommendation
    
    def _generate_summary(self, recommendations: List[Recommendation]) -> RecommendationSummary:
        """Generate summary statistics for recommendations."""
        total = len(recommendations)
        
        priority_counts = {"high": 0, "medium": 0, "low": 0}
        categories = set()
        
        for rec in recommendations:
            priority_counts[rec.priority.value] += 1
            categories.add(rec.test_category.value)
        
        return RecommendationSummary(
            total_recommendations=total,
            high_priority_count=priority_counts["high"],
            medium_priority_count=priority_counts["medium"],
            low_priority_count=priority_counts["low"],
            categories_covered=sorted(list(categories))
        )
    
    def _generate_educational_context(self, recommendation: Recommendation) -> str:
        """Generate educational context based on test details."""
        test_name = recommendation.test_name.lower()
        category = recommendation.test_category.value
        
        # Category-specific educational contexts
        category_contexts = {
            TestCategory.METABOLIC: "Metabolic tests assess how your body processes nutrients and maintains chemical balance, helping detect diabetes, kidney problems, and electrolyte imbalances.",
            TestCategory.LIPID_PROFILE: "Lipid testing evaluates your cardiovascular disease risk by measuring cholesterol and triglyceride levels, guiding heart-healthy lifestyle and treatment decisions.",
            TestCategory.VITAMINS: "Vitamin testing identifies deficiencies that can affect energy, immune function, bone health, and overall wellness. Most deficiencies are easily correctable with supplements.",
            TestCategory.HORMONES: "Hormone testing evaluates endocrine system function, affecting metabolism, reproduction, mood, and energy levels. Imbalances can often be treated effectively.",
            TestCategory.KIDNEY_FUNCTION: "Kidney function tests detect early signs of kidney disease, which often has no symptoms until advanced. Early detection allows for protective interventions.",
            TestCategory.LIVER_FUNCTION: "Liver function tests assess liver health and detect problems early. The liver processes toxins, makes proteins, and performs hundreds of vital functions.",
            TestCategory.COMPLETE_BLOOD_COUNT: "Complete blood count screens for anemia, infections, blood disorders, and immune system problems. It's a fundamental health assessment tool.",
            TestCategory.MINERALS: "Mineral testing evaluates essential nutrients like iron, calcium, and magnesium that support bone health, energy production, and cellular function.",
            TestCategory.TUMOR_MARKERS: "Tumor markers can help screen for certain cancers or monitor treatment response. Early detection significantly improves treatment outcomes.",
            TestCategory.INFLAMMATORY: "Inflammatory markers assess systemic inflammation, which contributes to heart disease, diabetes, and aging. Lifestyle changes can reduce inflammation.",
            TestCategory.CARDIOVASCULAR: "Cardiovascular tests evaluate heart disease risk factors beyond cholesterol, including inflammation and cardiac-specific proteins."
        }
        
        # Test-specific contexts
        test_contexts = {
            "glucose": "Blood glucose testing is essential for diabetes prevention and management. Early detection of prediabetes allows for lifestyle interventions to prevent progression.",
            "hba1c": "HbA1c reflects average blood sugar over 2-3 months, providing a comprehensive view of glucose control and diabetes risk.",
            "vitamin d": "Vitamin D is crucial for bone health, immune function, and may reduce risk of respiratory infections and autoimmune diseases.",
            "b12": "Vitamin B12 deficiency can cause fatigue, nerve problems, and anemia. It's especially common in vegetarians and older adults.",
            "cholesterol": "Cholesterol testing guides cardiovascular risk assessment and treatment decisions. High cholesterol is a major modifiable risk factor for heart disease.",
            "thyroid": "Thyroid function affects metabolism, energy, weight, mood, and heart rate. Both overactive and underactive thyroid are treatable conditions.",
            "creatinine": "Creatinine is a key marker of kidney function. Elevated levels may indicate kidney disease, which requires early intervention to prevent progression.",
            "psa": "PSA screening can help detect prostate cancer early when treatment is most effective, though it should be discussed with your healthcare provider."
        }
        
        # Try to find specific test context first
        for test_key, context in test_contexts.items():
            if test_key in test_name:
                return context
        
        # Fall back to category context
        if category in category_contexts:
            return category_contexts[category]
        
        # Generic fallback
        return f"Regular monitoring of {recommendation.test_name} helps maintain optimal health and detect potential issues early when they're most treatable."
    
    def _priority_to_score(self, priority: str) -> int:
        """Convert priority level to numeric score for sorting."""
        priority_scores = {"high": 3, "medium": 2, "low": 1}
        return priority_scores.get(priority.lower(), 1)
