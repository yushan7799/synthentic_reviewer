from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base

class Review(Base):
    """Review model representing a panelist's review of a proposal"""
    
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    
    # Foreign keys
    panelist_id = Column(Integer, ForeignKey('panelists.id'), nullable=False)
    proposal_id = Column(Integer, ForeignKey('proposals.id'), nullable=False)
    
    # Overall assessment
    overall_score = Column(Float, nullable=False)  # 1-10 scale
    recommendation = Column(String(50))  # accept, reject, revise
    
    # Category scores (1-10 scale)
    novelty_score = Column(Float)
    feasibility_score = Column(Float)
    impact_score = Column(Float)
    methodology_score = Column(Float)
    clarity_score = Column(Float)
    
    # Detailed feedback
    summary = Column(Text)
    strengths = Column(JSON)  # List of strengths
    weaknesses = Column(JSON)  # List of weaknesses
    detailed_comments = Column(Text)
    suggestions = Column(Text)
    
    # ReAct framework trace (for debugging/training)
    reasoning_trace = Column(JSON)
    
    # User feedback (for training)
    user_rating = Column(Float)  # How useful was this review (1-5)
    user_feedback = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def to_dict(self):
        """Convert review to dictionary"""
        return {
            'id': self.id,
            'panelist_id': self.panelist_id,
            'proposal_id': self.proposal_id,
            'overall_score': self.overall_score,
            'recommendation': self.recommendation,
            'scores': {
                'novelty': self.novelty_score,
                'feasibility': self.feasibility_score,
                'impact': self.impact_score,
                'methodology': self.methodology_score,
                'clarity': self.clarity_score
            },
            'feedback': {
                'summary': self.summary,
                'strengths': self.strengths or [],
                'weaknesses': self.weaknesses or [],
                'detailed_comments': self.detailed_comments,
                'suggestions': self.suggestions
            },
            'user_feedback': {
                'rating': self.user_rating,
                'comments': self.user_feedback
            },
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def get_average_score(self):
        """Calculate average of all category scores"""
        scores = [
            self.novelty_score,
            self.feasibility_score,
            self.impact_score,
            self.methodology_score,
            self.clarity_score
        ]
        valid_scores = [s for s in scores if s is not None]
        return sum(valid_scores) / len(valid_scores) if valid_scores else self.overall_score
