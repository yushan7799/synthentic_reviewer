from models.database import get_session
from models.review import Review
from typing import List, Dict, Any
import json

class TrainingService:
    """
    Service for training and improving the review system based on user feedback
    
    This is a placeholder for future ML training capabilities.
    Currently collects feedback for analysis.
    """
    
    def __init__(self):
        self.session = get_session()
    
    def collect_feedback_data(self) -> List[Dict[str, Any]]:
        """
        Collect all reviews with user feedback for training
        
        Returns:
            List of review data with feedback
        """
        reviews = self.session.query(Review).filter(
            Review.user_rating.isnot(None)
        ).all()
        
        training_data = []
        for review in reviews:
            training_data.append({
                'review_id': review.id,
                'panelist_id': review.panelist_id,
                'proposal_id': review.proposal_id,
                'scores': {
                    'overall': review.overall_score,
                    'novelty': review.novelty_score,
                    'feasibility': review.feasibility_score,
                    'impact': review.impact_score,
                    'methodology': review.methodology_score,
                    'clarity': review.clarity_score
                },
                'feedback': {
                    'summary': review.summary,
                    'strengths': review.strengths,
                    'weaknesses': review.weaknesses,
                    'detailed_comments': review.detailed_comments
                },
                'user_rating': review.user_rating,
                'user_feedback': review.user_feedback,
                'reasoning_trace': review.reasoning_trace
            })
        
        return training_data
    
    def analyze_feedback_patterns(self) -> Dict[str, Any]:
        """
        Analyze patterns in user feedback
        
        Returns:
            Dictionary with analysis results
        """
        training_data = self.collect_feedback_data()
        
        if not training_data:
            return {
                'total_reviews': 0,
                'average_rating': 0,
                'insights': []
            }
        
        # Calculate statistics
        ratings = [d['user_rating'] for d in training_data]
        avg_rating = sum(ratings) / len(ratings)
        
        # Identify high and low rated reviews
        high_rated = [d for d in training_data if d['user_rating'] >= 4]
        low_rated = [d for d in training_data if d['user_rating'] <= 2]
        
        insights = []
        
        # Analyze what makes good reviews
        if high_rated:
            insights.append({
                'type': 'positive',
                'message': f'{len(high_rated)} reviews received high ratings (4-5 stars)',
                'count': len(high_rated)
            })
        
        # Analyze what makes poor reviews
        if low_rated:
            insights.append({
                'type': 'negative',
                'message': f'{len(low_rated)} reviews received low ratings (1-2 stars)',
                'count': len(low_rated)
            })
        
        return {
            'total_reviews': len(training_data),
            'average_rating': avg_rating,
            'high_rated_count': len(high_rated),
            'low_rated_count': len(low_rated),
            'insights': insights,
            'training_data_available': len(training_data) >= 10
        }
    
    def suggest_improvements(self) -> List[str]:
        """
        Suggest improvements based on feedback analysis
        
        Returns:
            List of improvement suggestions
        """
        analysis = self.analyze_feedback_patterns()
        suggestions = []
        
        if analysis['total_reviews'] < 10:
            suggestions.append(
                "Collect more user feedback to enable meaningful training"
            )
        
        if analysis['average_rating'] < 3.5:
            suggestions.append(
                "Overall review quality is below target. Consider adjusting AI prompts."
            )
        
        if analysis['low_rated_count'] > analysis['high_rated_count']:
            suggestions.append(
                "More reviews are rated poorly than highly. Review generation logic needs improvement."
            )
        
        if analysis['training_data_available']:
            suggestions.append(
                "Sufficient training data available. Consider implementing fine-tuning."
            )
        
        return suggestions
    
    def export_training_data(self, filepath: str) -> bool:
        """
        Export training data to JSON file
        
        Args:
            filepath: Path to save the training data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            training_data = self.collect_feedback_data()
            
            with open(filepath, 'w') as f:
                json.dump(training_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error exporting training data: {e}")
            return False
    
    def get_panelist_performance(self, panelist_id: int) -> Dict[str, Any]:
        """
        Get performance metrics for a specific panelist
        
        Args:
            panelist_id: ID of the panelist
            
        Returns:
            Dictionary with performance metrics
        """
        reviews = self.session.query(Review).filter(
            Review.panelist_id == panelist_id,
            Review.user_rating.isnot(None)
        ).all()
        
        if not reviews:
            return {
                'panelist_id': panelist_id,
                'total_reviews': 0,
                'average_rating': 0,
                'performance': 'No data'
            }
        
        ratings = [r.user_rating for r in reviews]
        avg_rating = sum(ratings) / len(ratings)
        
        # Determine performance level
        if avg_rating >= 4:
            performance = 'Excellent'
        elif avg_rating >= 3:
            performance = 'Good'
        elif avg_rating >= 2:
            performance = 'Fair'
        else:
            performance = 'Needs Improvement'
        
        return {
            'panelist_id': panelist_id,
            'total_reviews': len(reviews),
            'average_rating': avg_rating,
            'performance': performance,
            'rating_distribution': {
                '5': len([r for r in ratings if r == 5]),
                '4': len([r for r in ratings if r == 4]),
                '3': len([r for r in ratings if r == 3]),
                '2': len([r for r in ratings if r == 2]),
                '1': len([r for r in ratings if r == 1])
            }
        }
