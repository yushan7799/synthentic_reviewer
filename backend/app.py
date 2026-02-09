from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models.database import init_db, get_session, close_session
from models.panelist import Panelist
from models.proposal import Proposal
from models.review import Review
from agents.profile_extractor import ProfileExtractor
from services.review_service import ReviewService
from utils.pdf_parser import PDFParser
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize database
init_db()

# Initialize services
profile_extractor = ProfileExtractor()
review_service = ReviewService()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# ============================================================================
# PANELIST ENDPOINTS
# ============================================================================

@app.route('/api/panelists', methods=['GET'])
def get_panelists():
    """Get all panelists"""
    try:
        session = get_session()
        panelists = session.query(Panelist).all()
        return jsonify({
            'success': True,
            'panelists': [p.to_dict() for p in panelists]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/panelists/<int:panelist_id>', methods=['GET'])
def get_panelist(panelist_id):
    """Get a specific panelist"""
    try:
        session = get_session()
        panelist = session.query(Panelist).get(panelist_id)
        if not panelist:
            return jsonify({'success': False, 'error': 'Panelist not found'}), 404
        return jsonify({
            'success': True,
            'panelist': panelist.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/panelists', methods=['POST'])
def create_panelist():
    """Create a new panelist"""
    try:
        data = request.json
        
        # Extract profile from URL if provided
        profile_data = {}
        if 'profile_url' in data and data['profile_url']:
            profile_data = profile_extractor.extract_profile(data['profile_url'])
            
            # Enhance with AI if extraction was successful
            if not profile_data.get('error'):
                profile_data = profile_extractor.enhance_with_ai(profile_data)
        
        # Create panelist
        session = get_session()
        panelist = Panelist(
            name=data.get('name') or profile_data.get('name', 'Unknown'),
            email=data.get('email', ''),
            profile_url=data.get('profile_url', ''),
            expertise_areas=data.get('expertise_areas') or profile_data.get('expertise_areas', []),
            publications=profile_data.get('publications', []),
            affiliations=profile_data.get('affiliations', []),
            bio=data.get('bio') or profile_data.get('bio', ''),
            critical_score=data.get('critical_score', 5.0),
            openness_score=data.get('openness_score', 5.0),
            seriousness_score=data.get('seriousness_score', 5.0)
        )
        
        session.add(panelist)
        session.commit()
        
        return jsonify({
            'success': True,
            'panelist': panelist.to_dict(),
            'profile_extraction': profile_data if profile_data else None
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/panelists/<int:panelist_id>', methods=['PUT'])
def update_panelist(panelist_id):
    """Update a panelist"""
    try:
        data = request.json
        session = get_session()
        panelist = session.query(Panelist).get(panelist_id)
        
        if not panelist:
            return jsonify({'success': False, 'error': 'Panelist not found'}), 404
        
        # Update fields
        if 'name' in data:
            panelist.name = data['name']
        if 'email' in data:
            panelist.email = data['email']
        if 'bio' in data:
            panelist.bio = data['bio']
        if 'expertise_areas' in data:
            panelist.expertise_areas = data['expertise_areas']
        if 'critical_score' in data:
            panelist.critical_score = data['critical_score']
        if 'openness_score' in data:
            panelist.openness_score = data['openness_score']
        if 'seriousness_score' in data:
            panelist.seriousness_score = data['seriousness_score']
        
        session.commit()
        
        return jsonify({
            'success': True,
            'panelist': panelist.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/panelists/<int:panelist_id>', methods=['DELETE'])
def delete_panelist(panelist_id):
    """Delete a panelist"""
    try:
        session = get_session()
        panelist = session.query(Panelist).get(panelist_id)
        
        if not panelist:
            return jsonify({'success': False, 'error': 'Panelist not found'}), 404
        
        session.delete(panelist)
        session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# PROPOSAL ENDPOINTS
# ============================================================================

@app.route('/api/proposals', methods=['GET'])
def get_proposals():
    """Get all proposals"""
    try:
        session = get_session()
        proposals = session.query(Proposal).all()
        return jsonify({
            'success': True,
            'proposals': [p.to_dict() for p in proposals]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/proposals/<int:proposal_id>', methods=['GET'])
def get_proposal(proposal_id):
    """Get a specific proposal"""
    try:
        session = get_session()
        proposal = session.query(Proposal).get(proposal_id)
        if not proposal:
            return jsonify({'success': False, 'error': 'Proposal not found'}), 404
        return jsonify({
            'success': True,
            'proposal': proposal.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/proposals/upload', methods=['POST'])
def upload_proposal():
    """Upload a proposal file"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Parse file
        if filename.endswith('.pdf'):
            parsed_data = PDFParser.extract_text(filepath)
        else:
            parsed_data = PDFParser.parse_text_file(filepath)
        
        # Create proposal
        session = get_session()
        proposal = Proposal(
            title=parsed_data.get('title', 'Untitled'),
            content=parsed_data.get('content', ''),
            abstract=parsed_data.get('abstract', ''),
            filename=filename,
            file_path=filepath,
            status='pending'
        )
        
        session.add(proposal)
        session.commit()
        
        return jsonify({
            'success': True,
            'proposal': proposal.to_dict()
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/proposals/<int:proposal_id>', methods=['DELETE'])
def delete_proposal(proposal_id):
    """Delete a proposal"""
    try:
        session = get_session()
        proposal = session.query(Proposal).get(proposal_id)
        
        if not proposal:
            return jsonify({'success': False, 'error': 'Proposal not found'}), 404
        
        # Delete file if exists
        if proposal.file_path and os.path.exists(proposal.file_path):
            os.remove(proposal.file_path)
        
        session.delete(proposal)
        session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# REVIEW ENDPOINTS
# ============================================================================

@app.route('/api/reviews/generate', methods=['POST'])
def generate_review():
    """Generate a review for a proposal"""
    try:
        data = request.json
        panelist_id = data.get('panelist_id')
        proposal_id = data.get('proposal_id')
        
        if not panelist_id or not proposal_id:
            return jsonify({'success': False, 'error': 'Missing panelist_id or proposal_id'}), 400
        
        review = review_service.generate_review(panelist_id, proposal_id)
        
        return jsonify({
            'success': True,
            'review': review.to_dict()
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reviews/panel', methods=['POST'])
def generate_panel_review():
    """Generate reviews from multiple panelists"""
    try:
        data = request.json
        proposal_id = data.get('proposal_id')
        panelist_ids = data.get('panelist_ids')  # Optional
        
        if not proposal_id:
            return jsonify({'success': False, 'error': 'Missing proposal_id'}), 400
        
        reviews = review_service.generate_panel_review(proposal_id, panelist_ids)
        
        return jsonify({
            'success': True,
            'reviews': [r.to_dict() for r in reviews],
            'count': len(reviews)
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reviews/proposal/<int:proposal_id>', methods=['GET'])
def get_proposal_reviews(proposal_id):
    """Get all reviews for a proposal"""
    try:
        summary = review_service.get_review_summary(proposal_id)
        return jsonify({
            'success': True,
            'summary': summary
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reviews/<int:review_id>/feedback', methods=['POST'])
def submit_review_feedback(review_id):
    """Submit feedback on a review"""
    try:
        data = request.json
        rating = data.get('rating')
        feedback = data.get('feedback', '')
        
        if rating is None:
            return jsonify({'success': False, 'error': 'Missing rating'}), 400
        
        review = review_service.submit_feedback(review_id, rating, feedback)
        
        return jsonify({
            'success': True,
            'review': review.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'ai_provider': Config.AI_PROVIDER
    })

@app.route('/api/extract-profile', methods=['POST'])
def extract_profile():
    """Extract profile from URL (for testing)"""
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({'success': False, 'error': 'Missing URL'}), 400
        
        profile_data = profile_extractor.extract_profile(url)
        
        if not profile_data.get('error'):
            profile_data = profile_extractor.enhance_with_ai(profile_data)
        
        return jsonify({
            'success': True,
            'profile': profile_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.teardown_appcontext
def shutdown_session(exception=None):
    """Close database session after request"""
    close_session()

if __name__ == '__main__':
    Config.init_app(app)
    app.run(debug=Config.DEBUG, port=5000)
