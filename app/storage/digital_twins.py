from typing import Dict
from app.models.digital_twin import DigitalTwin

# Shared in-memory storage for digital twins
# In production, this would be replaced with a database
digital_twins: Dict[str, DigitalTwin] = {}
