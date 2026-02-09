from models.database import get_session
from models.panelist import Panelist
from models.proposal import Proposal
from models.review import Review
from agents.panelist_agent import PanelistAgent
from typing import List, Dict, Any
import json

class ReviewService:
    """Service for generating and managing proposal reviews"""
    
    def __init__(self):
        self.session = get_session()
    
    def generate_review(
        self, 
        panelist_id: int, 
        proposal_id: int
    ) -> Review:
        """
        Generate a review for a proposal by a specific panelist
        
        Args:
            panelist_id: ID of the panelist
            proposal_id: ID of the proposal
            
        Returns:
            Review object
        """
        # Get panelist and proposal
        panelist = self.session.query(Panelist).get(panelist_id)
        proposal = self.session.query(Proposal).get(proposal_id)
        
        if not panelist or not proposal:
            raise ValueError("Panelist or proposal not found")
        
        # Create panelist agent
        agent = PanelistAgent(panelist.to_dict())
        
        # Generate review
        review_data = agent.review_proposal(proposal.to_dict())
        
        # Create review object
        review = Review(
            panelist_id=panelist_id,
            proposal_id=proposal_id,
            overall_score=review_data.get('overall_score', 5.0),
            recommendation=review_data.get('recommendation', 'revise'),
            novelty_score=review_data.get('novelty_score'),
            feasibility_score=review_data.get('feasibility_score'),
            impact_score=review_data.get('impact_score'),
            methodology_score=review_data.get('methodology_score'),
            clarity_score=review_data.get('clarity_score'),
            summary=review_data.get('summary', ''),
            strengths=review_data.get('strengths', []),
            weaknesses=review_data.get('weaknesses', []),
            detailed_comments=review_data.get('detailed_comments', ''),
            suggestions=review_data.get('suggestions', ''),
            reasoning_trace=review_data.get('reasoning_trace', [])
        )
        
        # Save to database
        self.session.add(review)
        self.session.commit()
        
        return review
    
    def generate_panel_review(
        self, 
        proposal_id: int, 
        panelist_ids: List[int] = None
    ) -> List[Review]:
        """
        Generate reviews from multiple panelists
        
        Args:
            proposal_id: ID of the proposal
            panelist_ids: List of panelist IDs (if None, use all panelists)
            
        Returns:
            List of Review objects
        """
        if panelist_ids is None:
            # Get all panelists
            panelists = self.session.query(Panelist).all()
            panelist_ids = [p.id for p in panelists]
        
        reviews = []
        for panelist_id in panelist_ids:
            try:
                review = self.generate_review(panelist_id, proposal_id)
                reviews.append(review)
            except Exception as e:
                print(f"Error generating review for panelist {panelist_id}: {e}")
                continue
        
        # Update proposal status
        proposal = self.session.query(Proposal).get(proposal_id)
        if proposal:
            proposal.status = 'completed'
            self.session.commit()
        
        return reviews
    
    def get_review_summary(self, proposal_id: int) -> Dict[str, Any]:
        """
        Get a summary of all reviews for a proposal
        
        Args:
            proposal_id: ID of the proposal
            
        Returns:
            Dictionary with review statistics and summaries
        """
        reviews = self.session.query(Review).filter_by(proposal_id=proposal_id).all()
        
        if not reviews:
            return {
                'proposal_id': proposal_id,
                'review_count': 0,
                'average_score': 0,
                'recommendation_breakdown': {},
                'reviews': []
            }
        
        # Calculate statistics
        scores = [r.overall_score for r in reviews]
        recommendations = [r.recommendation for r in reviews]
        
        recommendation_breakdown = {}
        for rec in recommendations:
            recommendation_breakdown[rec] = recommendation_breakdown.get(rec, 0) + 1
        
        # Get category averages
        category_scores = {
            'novelty': [r.novelty_score for r in reviews if r.novelty_score],
            'feasibility': [r.feasibility_score for r in reviews if r.feasibility_score],
            'impact': [r.impact_score for r in reviews if r.impact_score],
            'methodology': [r.methodology_score for r in reviews if r.methodology_score],
            'clarity': [r.clarity_score for r in reviews if r.clarity_score]
        }
        
        category_averages = {
            category: sum(scores) / len(scores) if scores else 0
            for category, scores in category_scores.items()
        }
        
        return {
            'proposal_id': proposal_id,
            'review_count': len(reviews),
            'average_score': sum(scores) / len(scores),
            'score_range': [min(scores), max(scores)],
            'recommendation_breakdown': recommendation_breakdown,
            'category_averages': category_averages,
            'reviews': [r.to_dict() for r in reviews]
        }
    
    def submit_feedback(
        self, 
        review_id: int, 
        rating: float, 
        feedback: str
    ) -> Review:
        """
        Submit user feedback on a review (for training)
        
        Args:
            review_id: ID of the review
            rating: User rating (1-5)
            feedback: User feedback text
            
        Returns:
            Updated Review object
        """
        review = self.session.query(Review).get(review_id)
        
        if not review:
            raise ValueError("Review not found")
        
        review.user_rating = rating
        review.user_feedback = feedback
        self.session.commit()
        
        return review
