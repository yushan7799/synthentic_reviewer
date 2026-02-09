# Developer Guide - Synthetic Reviewer

## 🛠️ Development Setup

### Initial Setup

1. **Clone and Navigate**
```bash
cd "/Users/yushanzhang/Desktop/synthetic reviewer"
```

2. **Run Setup Script**
```bash
chmod +x setup.sh
./setup.sh
```

3. **Configure API Keys**
Edit `backend/.env`:
```bash
# For OpenAI (recommended)
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...your-key-here...
OPENAI_MODEL=gpt-4-turbo-preview

# OR for Google Gemini
AI_PROVIDER=gemini
GEMINI_API_KEY=...your-key-here...
GEMINI_MODEL=gemini-pro
```

### Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```
Backend runs on: `http://localhost:5000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
Frontend runs on: `http://localhost:3000`

## 📂 Project Structure

```
synthetic-reviewer/
├── backend/                    # Python/Flask backend
│   ├── agents/                # AI agent implementations
│   │   ├── react_agent.py    # ReAct framework base
│   │   ├── panelist_agent.py # Panelist-specific agent
│   │   └── profile_extractor.py # Web scraping
│   ├── models/               # Database models
│   │   ├── database.py       # DB setup
│   │   ├── panelist.py       # Panelist model
│   │   ├── proposal.py       # Proposal model
│   │   └── review.py         # Review model
│   ├── services/             # Business logic
│   │   ├── openai_service.py # AI API wrapper
│   │   ├── review_service.py # Review generation
│   │   └── training_service.py # Analytics
│   ├── utils/                # Utilities
│   │   └── pdf_parser.py     # Document parsing
│   ├── app.py                # Main Flask app
│   ├── config.py             # Configuration
│   └── requirements.txt      # Dependencies
├── frontend/                  # React/Vite frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API client
│   │   ├── App.jsx           # Main app
│   │   ├── main.jsx          # Entry point
│   │   └── index.css         # Global styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── docs/                      # Documentation
    ├── README.md
    ├── IMPLEMENTATION_PLAN.md
    └── PROJECT_SUMMARY.md
```

## 🔧 Development Workflow

### Adding a New Panelist

1. **Backend**: Already implemented in `models/panelist.py`
2. **API**: Endpoint exists at `POST /api/panelists`
3. **Frontend**: Use `PanelistCreator` component

### Adding a New Review Category

1. **Update Model** (`backend/models/review.py`):
```python
new_category_score = Column(Float)
```

2. **Update Review Service** (`backend/services/review_service.py`):
```python
# Add to review generation logic
```

3. **Update Frontend** (`frontend/src/components/ReviewDisplay.jsx`):
```javascript
// Add to scores display
```

### Customizing AI Prompts

Edit `backend/agents/panelist_agent.py`:
```python
def _generate_structured_review(self, proposal):
    prompt = f"""
    # Customize this prompt
    You are reviewing a research proposal...
    """
```

## 🎨 Styling Guide

### Color System
```css
--primary: hsl(260, 85%, 60%)      /* Purple */
--secondary: hsl(200, 80%, 55%)    /* Blue */
--accent: hsl(340, 85%, 60%)       /* Pink */
--success: hsl(145, 70%, 55%)      /* Green */
--warning: hsl(40, 95%, 60%)       /* Yellow */
--error: hsl(0, 85%, 60%)          /* Red */
```

### Adding New Components

1. **Create Component File**:
```javascript
// frontend/src/components/MyComponent.jsx
import React from 'react';
import './MyComponent.css';

function MyComponent({ prop1, prop2 }) {
  return (
    <div className="my-component glass-card">
      {/* Component content */}
    </div>
  );
}

export default MyComponent;
```

2. **Create Styles**:
```css
/* frontend/src/components/MyComponent.css */
.my-component {
  /* Use existing CSS variables */
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
}
```

3. **Import in App**:
```javascript
import MyComponent from './components/MyComponent';
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
source venv/bin/activate
pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

### Manual Testing Checklist
- [ ] Create a panelist with profile URL
- [ ] Create a panelist manually
- [ ] Upload a PDF proposal
- [ ] Upload a text proposal
- [ ] Generate a single review
- [ ] Generate panel reviews
- [ ] View review summary
- [ ] Submit feedback on a review
- [ ] Delete a panelist
- [ ] Delete a proposal

## 🐛 Debugging

### Backend Debugging

**Enable Debug Mode**:
```python
# backend/config.py
DEBUG = True
```

**View Logs**:
```bash
# Flask logs appear in terminal
tail -f backend/app.log  # if logging to file
```

**Database Inspection**:
```bash
cd backend
python
>>> from models.database import get_session
>>> from models.panelist import Panelist
>>> session = get_session()
>>> panelists = session.query(Panelist).all()
>>> print(panelists)
```

### Frontend Debugging

**React DevTools**: Install browser extension

**Console Logging**:
```javascript
console.log('Debug:', data);
```

**Network Tab**: Check API calls in browser DevTools

## 📊 Database Management

### View Database
```bash
cd backend
sqlite3 synthetic_reviewer.db
.tables
SELECT * FROM panelists;
.quit
```

### Reset Database
```bash
cd backend
rm synthetic_reviewer.db
python
>>> from models.database import init_db
>>> init_db()
>>> exit()
```

### Backup Database
```bash
cp backend/synthetic_reviewer.db backend/backup_$(date +%Y%m%d).db
```

## 🚀 Deployment

### Backend Deployment (Heroku)

1. **Create Heroku App**:
```bash
cd backend
heroku create synthetic-reviewer-api
```

2. **Set Environment Variables**:
```bash
heroku config:set OPENAI_API_KEY=your-key
heroku config:set AI_PROVIDER=openai
```

3. **Create Procfile**:
```
web: gunicorn app:app
```

4. **Deploy**:
```bash
git push heroku main
```

### Frontend Deployment (Vercel)

1. **Install Vercel CLI**:
```bash
npm i -g vercel
```

2. **Deploy**:
```bash
cd frontend
vercel deploy --prod
```

3. **Update API URL**:
```javascript
// frontend/src/services/api.js
const API_BASE_URL = 'https://your-backend.herokuapp.com/api';
```

## 🔐 Environment Variables

### Backend (.env)
```bash
# Required
OPENAI_API_KEY=sk-...
AI_PROVIDER=openai

# Optional
DEBUG=True
DATABASE_URL=sqlite:///synthetic_reviewer.db
SECRET_KEY=your-secret-key
```

### Frontend
No environment variables needed for development.
For production, update API URL in `api.js`.

## 📝 Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints where appropriate
- Document functions with docstrings
- Keep functions focused and small

### JavaScript (Frontend)
- Use functional components
- Use hooks for state management
- Keep components under 300 lines
- Use meaningful variable names

### CSS
- Use CSS variables for theming
- Follow BEM naming convention
- Keep selectors specific but not overly nested
- Use flexbox and grid for layouts

## 🎯 Performance Tips

### Backend
- Use database indexes for frequently queried fields
- Cache API responses when appropriate
- Use async operations for long-running tasks
- Limit query results with pagination

### Frontend
- Lazy load components
- Memoize expensive calculations
- Debounce user inputs
- Optimize images and assets

## 🆘 Common Issues

### Issue: "Module not found"
**Solution**: 
```bash
cd backend
pip install -r requirements.txt
# OR
cd frontend
npm install
```

### Issue: "API key not found"
**Solution**: Check `backend/.env` file exists and contains valid API key

### Issue: "Database locked"
**Solution**: Close all connections and restart backend

### Issue: "CORS error"
**Solution**: Ensure Flask-CORS is installed and configured in `app.py`

### Issue: "Port already in use"
**Solution**: 
```bash
# Find and kill process
lsof -ti:5000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
```

## 📚 Additional Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Vite Documentation](https://vitejs.dev/)

### Learning
- ReAct Framework: [Paper](https://arxiv.org/abs/2210.03629)
- Prompt Engineering: [OpenAI Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- Modern CSS: [CSS Tricks](https://css-tricks.com/)

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request
5. Update documentation

## 📞 Support

For questions or issues:
1. Check this guide
2. Review error messages
3. Check browser console (frontend)
4. Check terminal output (backend)
5. Open an issue on GitHub

---

**Happy Coding! 🎉**
