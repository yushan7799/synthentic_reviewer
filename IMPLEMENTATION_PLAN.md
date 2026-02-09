# AI Proposal Review System - Implementation Plan

## Project Overview
A production-ready AI-powered system that simulates scientific proposal review processes using AI panelists with distinct personalities and expertise profiles.

## Core Features

### 1. Panelist Profile Creation
- Extract expertise from user-provided URLs (LinkedIn, Google Scholar, personal websites)
- Define personality traits:
  - Critical Score (1-10): How harsh/lenient in evaluation
  - Openness Score (1-10): Receptiveness to novel ideas
  - Seriousness Score (1-10): Formality and depth of analysis
- Store panelist profiles with their expertise areas

### 2. Proposal Review System
- Upload and parse research proposals (PDF/text)
- Assign proposals to AI panelists
- Generate reviews based on:
  - Panelist expertise
  - Personality traits
  - Proposal content
- Provide structured feedback with scores and comments

### 3. Training & Improvement
- Store historical reviews and proposals
- Learn from user feedback on review quality
- Refine panelist behavior over time

## Technology Stack

### Backend
- **Framework**: Flask (Python)
- **AI Integration**: OpenAI GPT-4 API (with Gemini as alternative)
- **Agent Framework**: ReAct (Reasoning + Acting)
- **Database**: SQLite for development, PostgreSQL for production
- **Web Scraping**: BeautifulSoup4, Selenium for profile extraction

### Frontend
- **Framework**: React with Vite
- **Styling**: Modern CSS with glassmorphism effects
- **UI Components**: Custom components with animations
- **State Management**: React Context API

## Project Structure

```
synthetic-reviewer/
├── backend/
│   ├── app.py                 # Flask application
│   ├── config.py              # Configuration
│   ├── requirements.txt       # Python dependencies
│   ├── agents/
│   │   ├── react_agent.py     # ReAct framework implementation
│   │   ├── panelist_agent.py  # Panelist behavior logic
│   │   └── profile_extractor.py # URL scraping & analysis
│   ├── models/
│   │   ├── database.py        # Database models
│   │   ├── panelist.py        # Panelist model
│   │   ├── proposal.py        # Proposal model
│   │   └── review.py          # Review model
│   ├── services/
│   │   ├── openai_service.py  # OpenAI API integration
│   │   ├── review_service.py  # Review generation logic
│   │   └── training_service.py # ML training pipeline
│   └── utils/
│       ├── pdf_parser.py      # PDF text extraction
│       └── validators.py      # Input validation
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   ├── components/
│   │   │   ├── PanelistCreator.jsx
│   │   │   ├── PanelistCard.jsx
│   │   │   ├── ProposalUploader.jsx
│   │   │   ├── ReviewDisplay.jsx
│   │   │   └── Dashboard.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   └── utils/
│   │       └── helpers.js
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Implementation Phases

### Phase 1: Backend Foundation (Core)
1. Set up Flask application structure
2. Implement database models
3. Create ReAct agent framework
4. Integrate OpenAI API
5. Build profile extraction from URLs

### Phase 2: Review Engine
1. Implement proposal parsing (PDF/text)
2. Create review generation logic with personality traits
3. Build scoring system
4. Add review storage and retrieval

### Phase 3: Frontend Development
1. Set up React + Vite project
2. Create stunning UI with modern design
3. Build panelist creation interface
4. Implement proposal upload and review display
5. Add dashboard for managing panelists and reviews

### Phase 4: Training & Enhancement
1. Implement feedback collection
2. Build training pipeline
3. Add review quality metrics
4. Create improvement loop

### Phase 5: Production Ready
1. Add comprehensive error handling
2. Implement authentication (optional)
3. Add API rate limiting
4. Create deployment configuration
5. Write documentation

## Key Design Decisions

### ReAct Framework Implementation
The system will use a ReAct (Reasoning + Acting) approach:
1. **Thought**: Analyze proposal content and panelist expertise
2. **Action**: Generate specific review components (scores, comments)
3. **Observation**: Evaluate generated content quality
4. **Reflection**: Adjust based on personality traits

### Personality Trait Integration
- **Critical Score**: Affects scoring harshness and comment tone
- **Openness Score**: Influences receptiveness to novel approaches
- **Seriousness Score**: Determines formality and depth of analysis

### Review Structure
Each review will include:
- Overall score (1-10)
- Category scores (novelty, feasibility, impact, methodology)
- Detailed comments
- Strengths and weaknesses
- Recommendations

## Next Steps
1. Initialize backend with Flask
2. Set up database models
3. Implement OpenAI integration
4. Create profile extraction service
5. Build frontend with React + Vite
