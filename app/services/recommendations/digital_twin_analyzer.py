from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import json
from pathlib import Path

from .models import (
    DigitalTwin, Demographics, BiomarkerSnapshot, BiomarkerValue,
    MedicalCondition, Medication, Supplement, FamilyCondition,
    LifestyleFactors, HealthGoal
)


class DigitalTwinAnalyzer:
    """Analyzes and aggregates user health data from multiple sources."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
    
    def load_user_data(self, user_id: str) -> DigitalTwin:
        """Load and aggregate all user data sources into a DigitalTwin object."""
        try:
            # Load demographics
            demographics = self._load_demographics(user_id)
            
            # Load biomarker data
            latest_biomarkers, biomarker_history = self._load_biomarker_data(user_id)
            
            # Load medical data
            conditions = self._load_conditions(user_id)
            medications = self._load_medications(user_id)
            supplements = self._load_supplements(user_id)
            family_history = self._load_family_history(user_id)
            
            # Load lifestyle data
            lifestyle = self._load_lifestyle(user_id)
            
            # Load goals
            goals = self._load_goals(user_id)
            
            return DigitalTwin(
                user_id=user_id,
                demographics=demographics,
                latest_biomarkers=latest_biomarkers,
                biomarker_history=biomarker_history,
                conditions=conditions,
                medications=medications,
                supplements=supplements,
                family_history=family_history,
                lifestyle=lifestyle,
                goals=goals
            )
        except Exception as e:
            # Return minimal digital twin with just user_id and basic demographics
            return DigitalTwin(
                user_id=user_id,
                demographics=Demographics(age=30, sex="unknown"),
                conditions=[],
                medications=[],
                supplements=[],
                family_history=[],
                goals=[]
            )
    
    def get_latest_biomarkers(self, twin: DigitalTwin) -> Optional[Dict[str, Any]]:
        """Get the most recent biomarker test results."""
        if twin.latest_biomarkers:
            return twin.latest_biomarkers.categories
        return None
    
    def get_biomarker_history(self, twin: DigitalTwin, marker: str, months: int = 12) -> List[Dict[str, Any]]:
        """Get historical values for a specific biomarker."""
        cutoff_date = datetime.now() - timedelta(days=months * 30)
        history = []
        
        for snapshot in twin.biomarker_history:
            if snapshot.test_date >= cutoff_date:
                # Search through categories for the marker
                for category, markers in snapshot.categories.items():
                    if marker in markers:
                        history.append({
                            "date": snapshot.test_date,
                            "value": markers[marker].value,
                            "unit": markers[marker].unit,
                            "status": markers[marker].status
                        })
        
        return sorted(history, key=lambda x: x["date"], reverse=True)
    
    def get_active_conditions(self, twin: DigitalTwin) -> List[MedicalCondition]:
        """Get currently active medical conditions."""
        return [c for c in twin.conditions if c.status == "active"]
    
    def calculate_time_since_test(self, twin: DigitalTwin, marker: str) -> Optional[timedelta]:
        """Calculate time since a biomarker was last tested."""
        if not twin.latest_biomarkers:
            return None
        
        # Search through categories for the marker
        for category, markers in twin.latest_biomarkers.categories.items():
            if marker in markers:
                return datetime.now() - twin.latest_biomarkers.test_date
        
        return None
    
    def _load_demographics(self, user_id: str) -> Demographics:
        """Load user demographics from data source."""
        # Try to load from user profile data
        try:
            profile_file = self.data_dir / f"{user_id}_profile.json"
            if profile_file.exists():
                with open(profile_file) as f:
                    data = json.load(f)
                return Demographics(**data.get("demographics", {"age": 30, "sex": "unknown"}))
        except:
            pass
        
        # Default demographics
        return Demographics(age=30, sex="unknown")
    
    def _load_biomarker_data(self, user_id: str) -> tuple[Optional[BiomarkerSnapshot], List[BiomarkerSnapshot]]:
        """Load biomarker data from data source."""
        try:
            biomarker_file = self.data_dir / f"{user_id}_biomarkers.json"
            if biomarker_file.exists():
                with open(biomarker_file) as f:
                    data = json.load(f)
                
                snapshots = []
                for item in data.get("biomarker_history", []):
                    # Convert biomarker values
                    categories = {}
                    for cat, markers in item.get("categories", {}).items():
                        categories[cat] = {
                            name: BiomarkerValue(**value) 
                            for name, value in markers.items()
                        }
                    
                    snapshot = BiomarkerSnapshot(
                        test_date=datetime.fromisoformat(item["test_date"]),
                        lab_name=item.get("lab_name", "Unknown Lab"),
                        test_package=item.get("test_package", "Standard Panel"),
                        categories=categories
                    )
                    snapshots.append(snapshot)
                
                # Sort by date, most recent first
                snapshots.sort(key=lambda x: x.test_date, reverse=True)
                latest = snapshots[0] if snapshots else None
                
                return latest, snapshots
        except:
            pass
        
        return None, []
    
    def _load_conditions(self, user_id: str) -> List[MedicalCondition]:
        """Load medical conditions from data source."""
        try:
            conditions_file = self.data_dir / f"{user_id}_conditions.json"
            if conditions_file.exists():
                with open(conditions_file) as f:
                    data = json.load(f)
                return [MedicalCondition(**item) for item in data.get("conditions", [])]
        except:
            pass
        return []
    
    def _load_medications(self, user_id: str) -> List[Medication]:
        """Load medications from data source."""
        try:
            meds_file = self.data_dir / f"{user_id}_medications.json"
            if meds_file.exists():
                with open(meds_file) as f:
                    data = json.load(f)
                return [Medication(**item) for item in data.get("medications", [])]
        except:
            pass
        return []
    
    def _load_supplements(self, user_id: str) -> List[Supplement]:
        """Load supplements from data source."""
        try:
            supps_file = self.data_dir / f"{user_id}_supplements.json"
            if supps_file.exists():
                with open(supps_file) as f:
                    data = json.load(f)
                return [Supplement(**item) for item in data.get("supplements", [])]
        except:
            pass
        return []
    
    def _load_family_history(self, user_id: str) -> List[FamilyCondition]:
        """Load family history from data source."""
        try:
            family_file = self.data_dir / f"{user_id}_family.json"
            if family_file.exists():
                with open(family_file) as f:
                    data = json.load(f)
                return [FamilyCondition(**item) for item in data.get("family_history", [])]
        except:
            pass
        return []
    
    def _load_lifestyle(self, user_id: str) -> Optional[LifestyleFactors]:
        """Load lifestyle data from data source."""
        try:
            lifestyle_file = self.data_dir / f"{user_id}_lifestyle.json"
            if lifestyle_file.exists():
                with open(lifestyle_file) as f:
                    data = json.load(f)
                return LifestyleFactors(**data.get("lifestyle", {}))
        except:
            pass
        return None
    
    def _load_goals(self, user_id: str) -> List[HealthGoal]:
        """Load health goals from data source."""
        try:
            goals_file = self.data_dir / f"{user_id}_goals.json"
            if goals_file.exists():
                with open(goals_file) as f:
                    data = json.load(f)
                return [HealthGoal(**item) for item in data.get("goals", [])]
        except:
            pass
        return []
