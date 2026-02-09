# Quick Reference - AI Models & Configuration

## 🤖 Default AI Models

### OpenAI (Default - Recommended)
```bash
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...your-key-here...
OPENAI_MODEL=gpt-4-turbo-preview
```

**Model Details:**
- **Name**: GPT-4 Turbo Preview
- **Context Window**: 128,000 tokens
- **Best For**: High-quality, detailed reviews
- **Cost**: ~$0.01 per 1K input tokens, ~$0.03 per 1K output tokens

**Alternative OpenAI Models:**
- `gpt-4` - Original GPT-4 (more expensive, 8K context)
- `gpt-3.5-turbo` - Faster and cheaper (good for testing)
- `gpt-4-1106-preview` - Latest GPT-4 Turbo

### Google Gemini (Alternative)
```bash
AI_PROVIDER=gemini
GEMINI_API_KEY=...your-key-here...
GEMINI_MODEL=gemini-pro
```

**Model Details:**
- **Name**: Gemini Pro
- **Context Window**: 32,000 tokens
- **Best For**: Cost-effective reviews
- **Cost**: Free tier available, then ~$0.00025 per 1K tokens

**Alternative Gemini Models:**
- `gemini-1.5-pro` - Latest version with larger context
- `gemini-1.5-flash` - Faster, lighter version

## 📝 Configuration File

Edit `backend/.env`:

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database
DATABASE_URL=sqlite:///synthetic_reviewer.db

# AI Provider Selection (choose one)
AI_PROVIDER=openai  # or 'gemini'

# OpenAI Configuration (if using OpenAI)
OPENAI_API_KEY=sk-proj-...your-key...
OPENAI_MODEL=gpt-4-turbo-preview

# Google Gemini Configuration (if using Gemini)
GEMINI_API_KEY=...your-key...
GEMINI_MODEL=gemini-pro
```

## 🔑 Getting API Keys

### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Add billing information (required for API access)

### Google Gemini API Key
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key
5. Free tier includes 60 requests per minute

## 💰 Cost Comparison

### For a typical review (assuming ~2000 tokens input, ~1500 tokens output):

**OpenAI GPT-4 Turbo:**
- Input: 2000 tokens × $0.01/1K = $0.02
- Output: 1500 tokens × $0.03/1K = $0.045
- **Total per review: ~$0.065**

**Google Gemini Pro:**
- Total: 3500 tokens × $0.00025/1K = $0.00088
- **Total per review: ~$0.001**

**Recommendation:**
- **Development/Testing**: Use Gemini Pro (cheaper)
- **Production**: Use GPT-4 Turbo (better quality)

## 🚀 Quick Start Commands

### 1. Install Dependencies (Already Done! ✅)
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
cd backend
cp .env.example .env
nano .env  # or use any text editor
# Add your API key
```

### 3. Start Backend
```bash
cd backend
source venv/bin/activate
python app.py
```

### 4. Start Frontend (New Terminal)
```bash
cd frontend
npm install  # first time only
npm run dev
```

### 5. Access Application
Open browser: http://localhost:3000

## 🔧 Switching Between AI Providers

Just change the `AI_PROVIDER` in `.env`:

```bash
# Use OpenAI
AI_PROVIDER=openai

# OR use Gemini
AI_PROVIDER=gemini
```

Restart the backend for changes to take effect.

## ✅ Installation Status

- ✅ Backend dependencies installed successfully
- ✅ SQLAlchemy 1.4.51 (no greenlet compilation issues)
- ✅ OpenAI SDK installed
- ✅ Google Gemini SDK installed
- ✅ All other dependencies ready

## 📊 Next Steps

1. **Get an API key** from OpenAI or Google
2. **Edit** `backend/.env` and add your key
3. **Start the backend**: `cd backend && source venv/bin/activate && python app.py`
4. **Install frontend deps**: `cd frontend && npm install`
5. **Start the frontend**: `npm run dev`
6. **Open browser**: http://localhost:3000

## 🆘 Troubleshooting

### "API key not found" error
- Check that `.env` file exists in `backend/` directory
- Verify the API key is correctly formatted
- Make sure there are no extra spaces

### "Module not found" error
- Run `pip install -r requirements.txt` again
- Make sure virtual environment is activated

### Port already in use
```bash
# Kill process on port 5000 (backend)
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

---

**You're all set! 🎉**

The greenlet compilation issue has been fixed by using SQLAlchemy 1.4.51 instead of 2.0.25.
All dependencies are now installed successfully!
