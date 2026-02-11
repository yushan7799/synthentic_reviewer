# 🚀 Quick Start Guide - Running the Application

## ⚠️ IMPORTANT: You Need to Add Your API Key First!

Before starting, edit `backend/.env` and add your OpenAI or Gemini API key:

```bash
# Open the file
nano backend/.env

# Or use any text editor
# Change this line:
OPENAI_API_KEY=your-openai-api-key-here

# To your actual key:
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
```

## 🎯 Starting the Application

### Terminal 1: Start Backend

```bash
cd "/Users/yushanzhang/Desktop/synthetic reviewer/backend"
source venv/bin/activate
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5001
* Debug mode: on
```

**Keep this terminal open!**

### Terminal 2: Start Frontend

```bash
cd "/Users/yushanzhang/Desktop/synthetic reviewer/frontend"
npm run dev
```

You should see:
```
VITE v5.0.8  ready in XXX ms

➜  Local:   http://localhost:3000/
```

**Keep this terminal open too!**

### Open Browser

Go to: **http://localhost:3000**

## 🔍 Troubleshooting

### Error: "Failed to extract profile"

**Cause**: Backend not running or API key not set

**Fix**:
1. Check Terminal 1 - is the backend running?
2. Check `backend/.env` - is your API key set?

### Error: "Unexpected end of JSON input"

**Cause**: Frontend can't connect to backend

**Fix**:
1. Make sure backend is running on port 5001
2. Refresh the browser page
3. Check browser console (F12) for errors

### Error: "Port 5001 already in use"

**Fix**:
```bash
lsof -ti:5001 | xargs kill -9
```

## ✅ How to Know It's Working

1. **Backend Terminal** shows:
   ```
   * Running on http://127.0.0.1:5001
   ```

2. **Frontend Terminal** shows:
   ```
   ➜  Local:   http://localhost:3000/
   ```

3. **Browser** at http://localhost:3000 shows the app

4. **Test the backend** (in a new terminal):
   ```bash
   curl http://localhost:5001/api/health
   ```
   Should return:
   ```json
   {"success":true,"status":"healthy","ai_provider":"openai"}
   ```

## 📝 Current Issue

Based on your screenshot, the backend is **NOT running**. 

**Solution**: Open a new terminal and run:
```bash
cd "/Users/yushanzhang/Desktop/synthetic reviewer/backend"
source venv/bin/activate
python app.py
```

Then try the "Extract" button again!

---

**Need help?** Check that:
- ✅ Backend terminal is running
- ✅ Frontend terminal is running  
- ✅ API key is set in `backend/.env`
- ✅ Browser is at http://localhost:3000
