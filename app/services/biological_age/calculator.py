from typing import Dict, Any
import math


class BiologicalAgeCalculator:
    """Calculates biological age from biomarkers and lifestyle factors"""
    
    # Evidence-based aging weights for different biomarker categories
    CATEGORY_WEIGHTS = {
        'metabolic': 0.25,      # HbA1c, glucose, insulin
        'cardiovascular': 0.25, # cholesterol, triglycerides, blood pressure
        'inflammatory': 0.20,   # CRP, inflammatory markers
        'hormonal': 0.15,       # testosterone, thyroid, cortisol
        'organ_function': 0.15  # kidney, liver function
    }
    
    def __init__(self):
        self.normalizer = BiomarkerNormalizer()
    
    def calculate_biological_age(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate biological age from user data"""
        chronological_age = user_data.get('age', 30)
        biomarkers = user_data.get('biomarkers', {})
        
        # Calculate age contributions by category
        metabolic_age = self._calculate_metabolic_age(biomarkers, chronological_age)
        cardiovascular_age = self._calculate_cardiovascular_age(biomarkers, chronological_age)
        inflammatory_age = self._calculate_inflammatory_age(biomarkers, chronological_age)
        hormonal_age = self._calculate_hormonal_age(biomarkers, chronological_age)
        organ_age = self._calculate_organ_function_age(biomarkers, chronological_age)
        
        # Weighted average
        biological_age = (
            metabolic_age * self.CATEGORY_WEIGHTS['metabolic'] +
            cardiovascular_age * self.CATEGORY_WEIGHTS['cardiovascular'] +
            inflammatory_age * self.CATEGORY_WEIGHTS['inflammatory'] +
            hormonal_age * self.CATEGORY_WEIGHTS['hormonal'] +
            organ_age * self.CATEGORY_WEIGHTS['organ_function']
        )
        
        age_delta = biological_age - chronological_age
        
        return {
            'chronological_age': chronological_age,
            'biological_age': round(biological_age, 1),
            'age_delta': round(age_delta, 1),
            'confidence_score': self._calculate_confidence(biomarkers),
            'category_ages': {
                'metabolic': round(metabolic_age, 1),
                'cardiovascular': round(cardiovascular_age, 1),
                'inflammatory': round(inflammatory_age, 1),
                'hormonal': round(hormonal_age, 1),
                'organ_function': round(organ_age, 1)
            }
        }
    
    def _calculate_metabolic_age(self, biomarkers: Dict[str, Any], base_age: int) -> float:
        """Calculate metabolic age from glucose, HbA1c"""
        age_adjustment = 0
        
        # Fasting glucose
        glucose = self._get_biomarker_value(biomarkers, 'fasting_glucose')
        if glucose:
            if glucose > 100:  # Pre-diabetic
                age_adjustment += 3
            if glucose > 126:  # Diabetic
                age_adjustment += 8
        
        # HbA1c
        hba1c = self._get_biomarker_value(biomarkers, 'hba1c')
        if hba1c:
            if hba1c > 5.7:  # Pre-diabetic
                age_adjustment += 4
            if hba1c > 6.5:  # Diabetic
                age_adjustment += 10
        
        return base_age + age_adjustment
    
    def _calculate_cardiovascular_age(self, biomarkers: Dict[str, Any], base_age: int) -> float:
        """Calculate cardiovascular age from lipid profile"""
        age_adjustment = 0
        
        # Total cholesterol
        total_chol = self._get_biomarker_value(biomarkers, 'total_cholesterol')
        if total_chol:
            if total_chol > 240:
                age_adjustment += 5
            elif total_chol > 200:
                age_adjustment += 2
        
        # HDL cholesterol (protective)
        hdl = self._get_biomarker_value(biomarkers, 'hdl_cholesterol')
        if hdl:
            if hdl < 40:  # Low HDL
                age_adjustment += 4
            elif hdl > 60:  # High HDL (protective)
                age_adjustment -= 2
        
        # Triglycerides
        triglycerides = self._get_biomarker_value(biomarkers, 'triglycerides')
        if triglycerides:
            if triglycerides > 200:
                age_adjustment += 3
            elif triglycerides > 150:
                age_adjustment += 1
        
        return base_age + age_adjustment
    
    def _calculate_inflammatory_age(self, biomarkers: Dict[str, Any], base_age: int) -> float:
        """Calculate inflammatory age from CRP and other markers"""
        age_adjustment = 0
        
        # CRP (if available in future data)
        # For now, use indirect markers
        
        # High triglycerides can indicate inflammation
        triglycerides = self._get_biomarker_value(biomarkers, 'triglycerides')
        if triglycerides and triglycerides > 200:
            age_adjustment += 2
        
        return base_age + age_adjustment
    
    def _calculate_hormonal_age(self, biomarkers: Dict[str, Any], base_age: int) -> float:
        """Calculate hormonal age from testosterone, thyroid"""
        age_adjustment = 0
        
        # Testosterone (gender-specific)
        testosterone = self._get_biomarker_value(biomarkers, 'testosterone')
        if testosterone:
            # Simplified - would need gender-specific ranges
            if testosterone < 300:  # Low for males
                age_adjustment += 3
        
        # TSH
        tsh = self._get_biomarker_value(biomarkers, 'tsh')
        if tsh:
            if tsh > 4.0:  # High TSH
                age_adjustment += 2
            elif tsh < 0.5:  # Low TSH
                age_adjustment += 1
        
        return base_age + age_adjustment
    
    def _calculate_organ_function_age(self, biomarkers: Dict[str, Any], base_age: int) -> float:
        """Calculate organ function age from kidney, liver markers"""
        age_adjustment = 0
        
        # Creatinine (kidney function)
        creatinine = self._get_biomarker_value(biomarkers, 'creatinine')
        if creatinine:
            if creatinine > 1.2:  # Elevated
                age_adjustment += 3
        
        # Liver enzymes
        alt = self._get_biomarker_value(biomarkers, 'sgpt_alt')
        if alt and alt > 40:
            age_adjustment += 2
        
        return base_age + age_adjustment
    
    def _get_biomarker_value(self, biomarkers: Dict[str, Any], name: str) -> float:
        """Extract biomarker value from data structure"""
        if name in biomarkers:
            data = biomarkers[name]
            if isinstance(data, dict) and 'value' in data:
                return float(data['value'])
            elif isinstance(data, (int, float)):
                return float(data)
        return None
    
    def _calculate_confidence(self, biomarkers: Dict[str, Any]) -> int:
        """Calculate confidence score based on available biomarkers"""
        key_markers = [
            'fasting_glucose', 'hba1c', 'total_cholesterol', 'hdl_cholesterol',
            'triglycerides', 'testosterone', 'tsh', 'creatinine'
        ]
        
        available = sum(1 for marker in key_markers if self._get_biomarker_value(biomarkers, marker) is not None)
        confidence = min(100, (available / len(key_markers)) * 100)
        return int(confidence)


class BiomarkerNormalizer:
    """Minimal normalizer for biological age calculation"""
    
    def normalize_biomarker(self, name: str, value: float, unit: str) -> float:
        """Basic normalization - can be expanded"""
        return value
