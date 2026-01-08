"""
Digital Twin database integration using SQLite.
Populates digital twins from the main database.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from app.models.digital_twin import DigitalTwin, FieldState
from app.services.user_db_service import user_db_service


class DigitalTwinDBService:
    """Create digital twins from SQLite database."""
    
    def get_or_create_digital_twin(self, user_id: str) -> Optional[DigitalTwin]:
        """Get or create a digital twin from database data."""
        user = user_db_service.get_user(user_id)
        if not user:
            return None
        
        # Create digital twin
        twin = DigitalTwin(user_id=user_id)
        
        # Populate demographics
        twin.set_value('demographics', 'age', user['age'])
        twin.set_value('demographics', 'gender', user['gender'])
        twin.set_value('demographics', 'city', user['city'])
        twin.set_value('demographics', 'height_cm', user['height_cm'])
        twin.set_value('demographics', 'weight_kg', user['weight_kg'])
        twin.set_value('demographics', 'bmi', user['bmi'])
        twin.set_value('demographics', 'blood_type', user['blood_type'])
        
        # Populate biomarkers
        biomarkers = user_db_service.get_user_biomarkers(user_id)
        for b in biomarkers:
            twin.set_value('biomarkers', b['name'], b['value'], unit=b['unit'], metadata={
                'normal_range': b['normal_range'],
                'status': b['status'],
                'category': b['category']
            })
        
        # Populate medical history
        history = user_db_service.get_user_medical_history(user_id)
        
        for condition in history.get('conditions', []):
            twin.set_value('medical_history', f"condition_{condition['name']}", condition['details'])
        
        for supp in history.get('supplements', []):
            twin.set_value('supplements', supp['name'], supp['details'])
        
        for fam in history.get('family_history', []):
            twin.set_value('family_history', fam['name'], fam['details'])
        
        return twin
    
    def get_digital_twin_summary(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a summary of the digital twin data."""
        twin = self.get_or_create_digital_twin(user_id)
        if not twin:
            return None
        
        domain_counts = {}
        total = 0
        for domain_name, domain in twin.domains.items():
            count = len(domain.fields)
            domain_counts[domain_name] = count
            total += count
        
        return {
            'user_id': user_id,
            'domains': domain_counts,
            'overall_completeness': twin.get_overall_completeness(),
            'total_data_points': total
        }
    
    def list_available_twins(self) -> List[Dict[str, Any]]:
        """List all users that can have digital twins."""
        users = user_db_service.get_all_users()
        result = []
        
        for user in users:
            biomarkers = user_db_service.get_user_biomarkers(user['user_id'])
            result.append({
                'user_id': user['user_id'],
                'age': user['age'],
                'gender': user['gender'],
                'data_source': user['data_source'],
                'biomarker_count': len(biomarkers),
                'has_data': len(biomarkers) > 0
            })
        
        return result


# Global instance
digital_twin_db = DigitalTwinDBService()
