import logging
from typing import Optional
from .models import RecommendationResponse
from .digital_twin_analyzer import DigitalTwinAnalyzer
from .recommendation_builder import RecommendationBuilder
from .priority_scorer import PriorityScorer
from .output_formatter import OutputFormatter

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Main recommendation engine service that orchestrates all components."""
    
    def __init__(self, data_dir: str = "data"):
        self.digital_twin_analyzer = DigitalTwinAnalyzer(data_dir)
        self.recommendation_builder = RecommendationBuilder()
        self.priority_scorer = PriorityScorer()
        self.output_formatter = OutputFormatter()
    
    def generate_recommendations(self, user_id: str) -> RecommendationResponse:
        """Generate comprehensive health recommendations for a user."""
        try:
            logger.info(f"Generating recommendations for user: {user_id}")
            
            # Step 1: Load and analyze digital twin data
            logger.info("Loading digital twin data...")
            digital_twin = self.digital_twin_analyzer.load_user_data(user_id)
            
            # Step 2: Build recommendations using all rule evaluators
            logger.info("Building recommendations...")
            recommendations = self.recommendation_builder.build_recommendations(digital_twin)
            
            # Step 3: Assign priority scores and levels
            logger.info("Scoring priorities...")
            scored_recommendations = self.priority_scorer.assign_priorities(recommendations, digital_twin)
            
            # Step 4: Format output
            logger.info("Formatting output...")
            response = self.output_formatter.format_recommendations(scored_recommendations, user_id)
            
            logger.info(f"Generated {len(recommendations)} recommendations for user {user_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error generating recommendations for user {user_id}: {str(e)}")
            return self._create_error_response(user_id, str(e))
    
    def _create_error_response(self, user_id: str, error_message: str) -> RecommendationResponse:
        """Create error response when recommendation generation fails."""
        from .models import RecommendationSummary
        from datetime import datetime
        
        return RecommendationResponse(
            user_id=user_id,
            generated_at=datetime.now(),
            summary=RecommendationSummary(
                total_recommendations=0,
                high_priority_count=0,
                medium_priority_count=0,
                low_priority_count=0,
                categories_covered=[]
            ),
            recommendations=[],
            grouped_by_category={}
        )
