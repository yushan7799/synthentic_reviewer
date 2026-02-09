from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from models.database import Base

class Proposal(Base):
    """Proposal model representing a research proposal to be reviewed"""
    
    __tablename__ = 'proposals'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    abstract = Column(Text)
    
    # File information
    filename = Column(String(255))
    file_path = Column(String(500))
    
    # Extracted metadata
    keywords = Column(JSON)  # List of keywords
    research_area = Column(String(200))
    
    # Status
    status = Column(String(50), default='pending')  # pending, reviewing, completed
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def to_dict(self):
        """Convert proposal to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'abstract': self.abstract,
            'filename': self.filename,
            'keywords': self.keywords or [],
            'research_area': self.research_area,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_summary(self):
        """Get a brief summary of the proposal"""
        summary = {
            'id': self.id,
            'title': self.title,
            'abstract': self.abstract[:200] + '...' if self.abstract and len(self.abstract) > 200 else self.abstract,
            'research_area': self.research_area,
            'status': self.status
        }
        return summary
