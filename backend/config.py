import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'sqlite:///synthetic_reviewer.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
    
    # Google Gemini (alternative)
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-pro')
    
    # AI Provider (openai or gemini)
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'openai')
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx'}
    
    # Review Settings
    MAX_PANELISTS = 10
    MIN_PANELISTS = 3
    DEFAULT_REVIEW_CATEGORIES = [
        'novelty',
        'feasibility', 
        'impact',
        'methodology',
        'clarity'
    ]
    
    # Web Scraping
    SCRAPING_TIMEOUT = 30
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    
    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
