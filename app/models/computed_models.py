"""
Database models for computed health data (routines, computed values).
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey, Text
from datetime import datetime
from app.database import Base


class ComputedData(Base):
    """Store computed/derived health data for users."""
    __tablename__ = "computed_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    data_type = Column(String(50), nullable=False)  # 'daily_routine', 'weekly_routine', 'health_score', etc.
    data = Column(JSON, nullable=False)
    computed_at = Column(DateTime, default=datetime.utcnow)
    version = Column(Integer, default=1)
