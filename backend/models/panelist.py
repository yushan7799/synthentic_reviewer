from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON
from sqlalchemy.sql import func
from models.database import Base
import json

class Panelist(Base):
    """Panelist model representing an AI reviewer"""
    
    __tablename__ = 'panelists'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200))
    profile_url = Column(String(500))
    
    # Extracted profile information
    expertise_areas = Column(JSON)  # List of expertise areas
    publications = Column(JSON)  # List of publications
    affiliations = Column(JSON)  # List of affiliations
    bio = Column(Text)
    
    # Personality traits (1-10 scale)
    critical_score = Column(Float, nullable=False, default=5.0)
    openness_score = Column(Float, nullable=False, default=5.0)
    seriousness_score = Column(Float, nullable=False, default=5.0)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def to_dict(self):
        """Convert panelist to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'profile_url': self.profile_url,
            'expertise_areas': self.expertise_areas or [],
            'publications': self.publications or [],
            'affiliations': self.affiliations or [],
            'bio': self.bio,
            'personality': {
                'critical_score': self.critical_score,
                'openness_score': self.openness_score,
                'seriousness_score': self.seriousness_score
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_personality_description(self):
        """Get human-readable personality description"""
        descriptions = []
        
        if self.critical_score >= 7:
            descriptions.append("highly critical and rigorous")
        elif self.critical_score <= 3:
            descriptions.append("supportive and encouraging")
        else:
            descriptions.append("balanced in critique")
            
        if self.openness_score >= 7:
            descriptions.append("very open to novel ideas")
        elif self.openness_score <= 3:
            descriptions.append("prefers traditional approaches")
        else:
            descriptions.append("moderately open to innovation")
            
        if self.seriousness_score >= 7:
            descriptions.append("extremely thorough and formal")
        elif self.seriousness_score <= 3:
            descriptions.append("casual and concise")
        else:
            descriptions.append("professional and focused")
            
        return ", ".join(descriptions)
