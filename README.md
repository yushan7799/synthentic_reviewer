# 🔬 Synthetic Reviewer

An AI-powered system that simulates scientific proposal review processes using AI panelists with distinct personalities and expertise profiles.

## ✨ Features

### 🤖 AI Panelist System
- **Profile Extraction**: Automatically extract expertise from LinkedIn, Google Scholar, and personal websites
- **Personality Traits**: Define reviewer characteristics with three key dimensions:
  - **Critical Score** (1-10): How harsh or supportive the reviewer is
  - **Openness Score** (1-10): Receptiveness to novel and unconventional ideas
  - **Seriousness Score** (1-10): Formality and thoroughness of analysis
- **Expertise Modeling**: Store publications, affiliations, and research areas

### 📝 Proposal Review
- **Multi-Format Support**: Upload proposals in PDF, TXT, DOC, or DOCX format
- **Automated Parsing**: Extract title, abstract, and content automatically
- **Panel Reviews**: Generate reviews from multiple panelists simultaneously
- **Structured Feedback**: Get comprehensive reviews including:
  - Overall score and recommendation (accept/revise/reject)
  - Category scores (novelty, feasibility, impact, methodology, clarity)
  - Detailed strengths and weaknesses
  - Constructive suggestions for improvement

### 🧠 ReAct Framework
- **Reasoning + Acting**: AI agents follow a structured thought process
- **Transparent Decision Making**: View the reasoning trace behind each review
- **Personality-Driven**: Reviews adapt based on panelist personality traits

### 📊 Analytics & Insights
- **Review Summaries**: Aggregate statistics across all panelists
- **Score Distributions**: Visualize recommendation breakdowns
- **Category Averages**: Compare performance across evaluation dimensions

### 🎨 Modern UI
- **Dark Theme**: Eye-friendly glassmorphism design
- **Smooth Animations**: Engaging micro-interactions
- **Responsive**: Works on desktop, tablet, and mobile
- **Intuitive Navigation**: Easy-to-use dashboard interface

## 🏗️ Architecture

### Backend (Python/Flask)
```
backend/
├── app.py                      # Main Flask application
├── config.py                   # Configuration management
├── models/                     # Database models
│   ├── panelist.py            # Panelist model
│   ├── proposal.py            # Proposal model
│   └── review.py              # Review model
├── agents/                     # AI agents
│   ├── react_agent.py         # ReAct framework
│   ├── panelist_agent.py      # Panelist behavior
│   └── profile_extractor.py   # Web scraping
├── services/                   # Business logic
│   ├── openai_service.py      # AI integration
│   └── review_service.py      # Review generation
└── utils/                      # Utilities
    └── pdf_parser.py          # Document parsing
```

### Frontend (React/Vite)
```
frontend/
├── src/
│   ├── App.jsx                # Main application
│   ├── components/            # React components
│   │   ├── PanelistCreator.jsx
│   │   ├── PanelistCard.jsx
│   │   ├── ProposalUploader.jsx
│   │   └── ReviewDisplay.jsx
│   └── services/
│       └── api.js             # API client
└── index.html
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key or Google Gemini API key

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
OPENAI_API_KEY=your-openai-api-key-here
# OR
GEMINI_API_KEY=your-gemini-api-key-here
AI_PROVIDER=openai  # or gemini
```

5. **Run the backend**:
```bash
python app.py
```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Run the development server**:
```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

## 📖 Usage Guide

### 1. Create AI Panelists

1. Navigate to **Create Panelist** tab
2. Enter a profile URL (LinkedIn, Google Scholar, etc.) and click **Extract**
3. The system will automatically extract:
   - Name and bio
   - Expertise areas
   - Publications
   - Affiliations
4. Adjust personality traits using the sliders:
   - **Critical Score**: Higher = more critical reviews
   - **Openness Score**: Higher = more receptive to novel ideas
   - **Seriousness Score**: Higher = more thorough and formal
5. Click **Create Panelist**

### 2. Upload a Proposal

1. Navigate to **Upload Proposal** tab
2. Drag and drop a file or click to browse
3. Supported formats: PDF, TXT, DOC, DOCX
4. The system will automatically extract:
   - Title
   - Abstract
   - Full content
5. Click **Upload Proposal**

### 3. Generate Reviews

1. Navigate to **Reviews** tab
2. Select a proposal from the list
3. Choose specific panelists or generate reviews from all panelists
4. Click **Generate Reviews**
5. Wait for the AI to generate comprehensive reviews

### 4. View Results

- **Summary Statistics**: Overall scores, recommendation breakdown, category averages
- **Individual Reviews**: Detailed feedback from each panelist including:
  - Overall score and recommendation
  - Category scores
  - Strengths and weaknesses
  - Detailed comments
  - Suggestions for improvement

## 🔧 Configuration

### AI Provider Selection

The system supports both OpenAI and Google Gemini. Configure in `.env`:

```bash
# For OpenAI
AI_PROVIDER=openai
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-4-turbo-preview

# For Google Gemini
AI_PROVIDER=gemini
GEMINI_API_KEY=your-key
GEMINI_MODEL=gemini-pro
```

### Database Configuration

By default, the system uses SQLite. For production, use PostgreSQL:

```bash
DATABASE_URL=postgresql://user:password@localhost/synthetic_reviewer
```

## 🎯 API Endpoints

### Panelists
- `GET /api/panelists` - Get all panelists
- `POST /api/panelists` - Create a panelist
- `GET /api/panelists/:id` - Get a specific panelist
- `PUT /api/panelists/:id` - Update a panelist
- `DELETE /api/panelists/:id` - Delete a panelist

### Proposals
- `GET /api/proposals` - Get all proposals
- `POST /api/proposals/upload` - Upload a proposal
- `GET /api/proposals/:id` - Get a specific proposal
- `DELETE /api/proposals/:id` - Delete a proposal

### Reviews
- `POST /api/reviews/generate` - Generate a single review
- `POST /api/reviews/panel` - Generate panel reviews
- `GET /api/reviews/proposal/:id` - Get all reviews for a proposal
- `POST /api/reviews/:id/feedback` - Submit user feedback

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚢 Deployment

### Backend (Heroku)
```bash
cd backend
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your-key
git push heroku main
```

### Frontend (Vercel)
```bash
cd frontend
vercel deploy
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with OpenAI GPT-4 and Google Gemini
- Inspired by real scientific review processes
- Uses the ReAct (Reasoning + Acting) framework

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ for the research community**
