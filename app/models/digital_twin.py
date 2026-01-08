from enum import Enum
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


class FieldState(Enum):
    POPULATED = "populated"
    MISSING = "missing"
    NOT_APPLICABLE = "not_applicable"


class HealthDataPoint:
    def __init__(self, value: Any, timestamp: datetime, unit: Optional[str] = None, metadata: Dict[str, Any] = None):
        self.value = value
        self.timestamp = timestamp
        self.unit = unit
        self.metadata = metadata or {}


class HealthField:
    def __init__(self, field_name: str, field_type: str, state: FieldState):
        self.field_name = field_name
        self.field_type = field_type
        self.state = state
        self.values: List[HealthDataPoint] = []
    
    def add_value(self, value: Any, timestamp: datetime, unit: Optional[str] = None, metadata: Dict[str, Any] = None):
        """Add a new data point to this field"""
        data_point = HealthDataPoint(
            value=value,
            timestamp=timestamp,
            unit=unit,
            metadata=metadata or {}
        )
        self.values.append(data_point)
        self.values.sort(key=lambda x: x.timestamp)
        self.state = FieldState.POPULATED
    
    def get_latest_value(self) -> Optional[HealthDataPoint]:
        """Get the most recent data point"""
        return self.values[-1] if self.values else None
    
    def get_historical_values(self) -> List[HealthDataPoint]:
        """Get all data points in chronological order"""
        return self.values


class HealthDomain:
    def __init__(self, domain_name: str):
        self.domain_name = domain_name
        self.fields: Dict[str, HealthField] = {}
    
    def add_field(self, field_name: str, field_type: str, state: FieldState = FieldState.MISSING):
        """Add a new field to this domain"""
        self.fields[field_name] = HealthField(
            field_name=field_name,
            field_type=field_type,
            state=state
        )
    
    def set_field_value(self, field_name: str, value: Any, timestamp: datetime, unit: Optional[str] = None, metadata: Dict[str, Any] = None):
        """Set value for a field, creating it if it doesn't exist"""
        if field_name not in self.fields:
            self.add_field(field_name, type(value).__name__)
        
        self.fields[field_name].add_value(value, timestamp, unit, metadata)
    
    def get_missing_fields(self) -> List[str]:
        """Get list of missing field names"""
        return [name for name, field in self.fields.items() if field.state == FieldState.MISSING]
    
    def get_completeness_percentage(self) -> float:
        """Calculate data completeness percentage for this domain"""
        if not self.fields:
            return 0.0
        
        populated_count = sum(1 for field in self.fields.values() if field.state == FieldState.POPULATED)
        return (populated_count / len(self.fields)) * 100


class DigitalTwin:
    def __init__(self, user_id: str, metadata: Dict[str, Any] = None):
        self.user_id = user_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.metadata = metadata or {}
        self.domains: Dict[str, HealthDomain] = {}
        
        # Initialize common health domains
        common_domains = ["demographics", "biomarkers", "medical_history", "lifestyle", "genetics"]
        for domain_name in common_domains:
            self.domains[domain_name] = HealthDomain(domain_name=domain_name)
    
    def set_value(self, domain: str, field: str, value: Any, timestamp: Optional[datetime] = None, unit: Optional[str] = None, metadata: Dict[str, Any] = None):
        """Add data to any domain/field"""
        if timestamp is None:
            timestamp = datetime.now()
        
        if domain not in self.domains:
            self.domains[domain] = HealthDomain(domain_name=domain)
        
        self.domains[domain].set_field_value(field, value, timestamp, unit, metadata)
        self.updated_at = datetime.now()
    
    def get_value(self, domain: str, field: str, latest: bool = True) -> Union[HealthDataPoint, List[HealthDataPoint], None]:
        """Get value from a specific domain/field"""
        if domain not in self.domains or field not in self.domains[domain].fields:
            return None
        
        health_field = self.domains[domain].fields[field]
        if latest:
            return health_field.get_latest_value()
        else:
            return health_field.get_historical_values()
    
    def get_domain(self, domain: str) -> Optional[HealthDomain]:
        """Retrieve entire domain"""
        return self.domains.get(domain)
    
    def get_missing_fields(self) -> Dict[str, List[str]]:
        """List missing fields across all domains"""
        missing_fields = {}
        for domain_name, domain in self.domains.items():
            missing = domain.get_missing_fields()
            if missing:
                missing_fields[domain_name] = missing
        return missing_fields
    
    def get_overall_completeness(self) -> float:
        """Calculate overall data completeness percentage"""
        if not self.domains:
            return 0.0
        
        total_completeness = sum(domain.get_completeness_percentage() for domain in self.domains.values())
        return total_completeness / len(self.domains)
