"""
Database models for user health data.
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    age = Column(Integer)
    gender = Column(String(1))
    city = Column(String(100))
    country = Column(String(100), default="India")
    height_cm = Column(Float)
    weight_kg = Column(Float)
    bmi = Column(Float)
    blood_type = Column(String(5))
    biological_age = Column(Float)
    data_source = Column(String(50))  # 'hardcoded', 'ocr', 'manual'
    preferred_language = Column(String(5), default='en')  # User's preferred language
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    biomarkers = relationship("Biomarker", back_populates="user", cascade="all, delete-orphan")
    medical_history = relationship("MedicalHistory", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    translations = relationship("UserTranslation", back_populates="user", cascade="all, delete-orphan")


class Biomarker(Base):
    __tablename__ = "biomarkers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(50))
    normal_range = Column(String(50))
    status = Column(String(20))  # 'normal', 'high', 'low'
    category = Column(String(50))  # 'metabolic', 'lipids', 'vitamins', etc.
    test_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="biomarkers")


class MedicalHistory(Base):
    __tablename__ = "medical_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    type = Column(String(50))  # 'condition', 'medication', 'supplement', 'family_history'
    name = Column(String(200), nullable=False)
    details = Column(JSON)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="medical_history")


class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    type = Column(String(100))
    target = Column(Text)
    status = Column(String(20), default="active")
    start_date = Column(DateTime)
    target_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="goals")


class UserTranslation(Base):
    """
    Store pre-computed translations for user-specific content
    """
    __tablename__ = "user_translations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    content_type = Column(String(50), nullable=False)  # 'recommendation', 'insight', 'biomarker_name', etc.
    content_key = Column(String(200), nullable=False)  # Unique identifier for the content
    language = Column(String(5), nullable=False)  # 'en', 'hi', 'ta'
    original_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="translations")
    
    # Create composite index for fast lookups
    __table_args__ = (
        Index('idx_user_content_lang', 'user_id', 'content_type', 'content_key', 'language'),
        Index('idx_user_lang', 'user_id', 'language'),
    )
