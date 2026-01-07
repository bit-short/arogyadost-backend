from typing import Dict, Any, Optional
import math


class BiomarkerNormalizer:
    """Normalizes biomarker values to standard units and validates ranges"""
    
    # Physiologically possible ranges (min, max)
    VALID_RANGES = {
        'albumin_g_per_l': (20, 60),
        'creatinine_umol_per_l': (40, 400),
        'glucose_mmol_per_l': (2.0, 30.0),
        'crp_mg_per_l': (0.0, 100.0),
        'cholesterol_mmol_per_l': (2.0, 15.0),
        'hdl_mmol_per_l': (0.5, 3.0),
        'ldl_mmol_per_l': (1.0, 10.0),
        'triglycerides_mmol_per_l': (0.3, 10.0),
        'hemoglobin_g_per_l': (80, 200),
        'vitamin_d_nmol_per_l': (10, 500)
    }
    
    def normalize_albumin(self, value: float, from_unit: str = "g/dL") -> float:
        """Convert albumin to g/L"""
        if from_unit == "g/dL":
            result = value * 10  # g/dL to g/L
        elif from_unit == "g/L":
            result = value
        else:
            raise ValueError(f"Unsupported albumin unit: {from_unit}")
        
        self._validate_range(result, 'albumin_g_per_l')
        return result
    
    def normalize_creatinine(self, value: float, from_unit: str = "mg/dL") -> float:
        """Convert creatinine to µmol/L"""
        if from_unit == "mg/dL":
            result = value * 88.4  # mg/dL to µmol/L
        elif from_unit == "µmol/L" or from_unit == "umol/L":
            result = value
        else:
            raise ValueError(f"Unsupported creatinine unit: {from_unit}")
        
        self._validate_range(result, 'creatinine_umol_per_l')
        return result
    
    def normalize_glucose(self, value: float, from_unit: str = "mg/dL") -> float:
        """Convert glucose to mmol/L"""
        if from_unit == "mg/dL":
            result = value * 0.0555  # mg/dL to mmol/L
        elif from_unit == "mmol/L":
            result = value
        else:
            raise ValueError(f"Unsupported glucose unit: {from_unit}")
        
        self._validate_range(result, 'glucose_mmol_per_l')
        return result
    
    def normalize_crp(self, value: float, from_unit: str = "mg/dL") -> float:
        """Convert CRP to mg/L"""
        if from_unit == "mg/dL":
            result = value * 10  # mg/dL to mg/L
        elif from_unit == "mg/L":
            result = value
        else:
            raise ValueError(f"Unsupported CRP unit: {from_unit}")
        
        self._validate_range(result, 'crp_mg_per_l')
        return result
    
    def normalize_cholesterol(self, value: float, from_unit: str = "mg/dL") -> float:
        """Convert cholesterol to mmol/L"""
        if from_unit == "mg/dL":
            result = value * 0.0259  # mg/dL to mmol/L
        elif from_unit == "mmol/L":
            result = value
        else:
            raise ValueError(f"Unsupported cholesterol unit: {from_unit}")
        
        self._validate_range(result, 'cholesterol_mmol_per_l')
        return result
    
    def normalize_hdl(self, value: float, from_unit: str = "mg/dL") -> float:
        """Convert HDL to mmol/L"""
        if from_unit == "mg/dL":
            result = value * 0.0259  # mg/dL to mmol/L
        elif from_unit == "mmol/L":
            result = value
        else:
            raise ValueError(f"Unsupported HDL unit: {from_unit}")
        
        self._validate_range(result, 'hdl_mmol_per_l')
        return result
    
    def normalize_ldl(self, value: float, from_unit: str = "mg/dL") -> float:
        """Convert LDL to mmol/L"""
        if from_unit == "mg/dL":
            result = value * 0.0259  # mg/dL to mmol/L
        elif from_unit == "mmol/L":
            result = value
        else:
            raise ValueError(f"Unsupported LDL unit: {from_unit}")
        
        self._validate_range(result, 'ldl_mmol_per_l')
        return result
    
    def normalize_triglycerides(self, value: float, from_unit: str = "mg/dL") -> float:
        """Convert triglycerides to mmol/L"""
        if from_unit == "mg/dL":
            result = value * 0.0113  # mg/dL to mmol/L
        elif from_unit == "mmol/L":
            result = value
        else:
            raise ValueError(f"Unsupported triglycerides unit: {from_unit}")
        
        self._validate_range(result, 'triglycerides_mmol_per_l')
        return result
    
    def normalize_hemoglobin(self, value: float, from_unit: str = "g/dL") -> float:
        """Convert hemoglobin to g/L"""
        if from_unit == "g/dL":
            result = value * 10  # g/dL to g/L
        elif from_unit == "g/L":
            result = value
        else:
            raise ValueError(f"Unsupported hemoglobin unit: {from_unit}")
        
        self._validate_range(result, 'hemoglobin_g_per_l')
        return result
    
    def normalize_vitamin_d(self, value: float, from_unit: str = "ng/mL") -> float:
        """Convert vitamin D to nmol/L"""
        if from_unit == "ng/mL":
            result = value * 2.5  # ng/mL to nmol/L
        elif from_unit == "nmol/L":
            result = value
        else:
            raise ValueError(f"Unsupported vitamin D unit: {from_unit}")
        
        self._validate_range(result, 'vitamin_d_nmol_per_l')
        return result
    
    def normalize_biomarker(self, biomarker_name: str, value: float, from_unit: str) -> float:
        """Generic biomarker normalization"""
        normalizers = {
            'albumin': self.normalize_albumin,
            'creatinine': self.normalize_creatinine,
            'glucose': self.normalize_glucose,
            'fasting_glucose': self.normalize_glucose,
            'crp': self.normalize_crp,
            'total_cholesterol': self.normalize_cholesterol,
            'hdl_cholesterol': self.normalize_hdl,
            'ldl_cholesterol': self.normalize_ldl,
            'triglycerides': self.normalize_triglycerides,
            'hemoglobin': self.normalize_hemoglobin,
            'vitamin_d': self.normalize_vitamin_d
        }
        
        normalizer = normalizers.get(biomarker_name)
        if normalizer:
            return normalizer(value, from_unit)
        else:
            # Return as-is for unsupported biomarkers
            return value
    
    def _validate_range(self, value: float, range_key: str):
        """Validate that value is within physiologically possible range"""
        if range_key in self.VALID_RANGES:
            min_val, max_val = self.VALID_RANGES[range_key]
            if not (min_val <= value <= max_val):
                raise ValueError(f"Value {value} outside valid range [{min_val}, {max_val}] for {range_key}")
    
    def get_normalized_biomarkers(self, biomarkers: Dict[str, Any]) -> Dict[str, float]:
        """Normalize all biomarkers in a dictionary"""
        normalized = {}
        
        for name, data in biomarkers.items():
            if isinstance(data, dict) and 'value' in data:
                value = data['value']
                unit = data.get('unit', 'unknown')
                
                try:
                    normalized[name] = self.normalize_biomarker(name, value, unit)
                except (ValueError, TypeError):
                    # Skip biomarkers that can't be normalized
                    normalized[name] = value
            elif isinstance(data, (int, float)):
                normalized[name] = float(data)
        
        return normalized
