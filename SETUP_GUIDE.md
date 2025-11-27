# 🚀 Complete Setup Guide - AI Tutor Platform

## Step 1: Create Project Structure

```bash
# Create main directory
mkdir ai_tutor_platform
cd ai_tutor_platform

# Create subdirectories
mkdir backend frontend test_samples
```

## Step 2: Setup Backend

### Create Backend Files

Navigate to backend directory and create files:

```bash
cd backend
```

Create these files (copy content from artifacts):
1. `main.py` - Main FastAPI application
2. `ai_engine.py` - AI analysis engine
3. `language_detector.py` - Language detection module
4. `static_analyzer.py` - Static code analysis
5. `requirements.txt` - Python dependencies

### Install Backend Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install python-multipart==0.0.6
pip install pydantic==2.5.0
pip install python-dotenv==1.0.0
```

### (Optional) Setup API Keys

If you want real LLM analysis:

```bash
# Create .env file
touch .env

# Edit .env and add:
# OPENAI_API_KEY=your_key_here
# OR
# ANTHROPIC_API_KEY=your_key_here
```

### Start Backend Server

```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

Test it:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy","service":"AI Tutor Platform","ai_engine":"ready"}
```

## Step 3: Setup Frontend

Open a NEW terminal (keep backend running).

### Create Frontend Files

```bash
cd frontend  # from project root
```

Create these files:
1. `app.py` - Streamlit application
2. `requirements.txt` - Frontend dependencies

### Install Frontend Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install streamlit==1.29.0
pip install requests==2.31.0
```

### Start Frontend

```bash
streamlit run app.py
```

You should see:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Your browser should automatically open to `http://localhost:8501`

## Step 4: Create Test Files

Navigate to test_samples and create sample files:

```bash
cd test_samples  # from project root
```

Create these test files (copy content from artifacts):
1. `sample.py` - Python test file
2. `sample.js` - JavaScript test file
3. `sample.html` - HTML test file
4. `sample.java` - Java test file
5. `sample.dart` - Flutter/Dart test file

## Step 5: Test the Platform

1. **Open the UI**: Go to `http://localhost:8501`

2. **Check API Status**: Look at the sidebar - should show "✅ API Connected"

3. **Upload Test File**: 
   - Click "Choose a code file"
   - Select `test_samples/sample.py`
   - You'll see a code preview

4. **Analyze Code**:
   - Click "🚀 Analyze Code" button
   - Wait for analysis (2-5 seconds)

5. **View Results**:
   - Score out of 100
   - Letter grade
   - Detected language
   - Errors (if any)
   - Recommendations
   - Strengths

6. **Try Other Files**:
   - Test with `sample.js`
   - Test with `sample.html`
   - Test with your own code files

## Step 6: Verify Everything Works

### Backend Health Check
```bash
curl http://localhost:8000/health
```

### Frontend UI Check
- Open `http://localhost:8501`
- Sidebar shows "✅ API Connected"
- File upload button visible

### End-to-End Test
```bash
# Test API directly with curl
curl -X POST "http://localhost:8000/analyze-code" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_samples/sample.py"
```

Should return JSON with analysis results.

## 📊 Expected Results for Sample Files

### sample.py (Python)
- **Score**: ~75-85
- **Grade**: B or C
- **Errors**: Minimal (well-structured code)
- **Recommendations**: Add type hints, more comments

### sample.js (JavaScript)
- **Score**: ~60-70
- **Grade**: C or D
- **Errors**: Uses `var` instead of `const/let`
- **Recommendations**: Use modern ES6+, strict equality

### sample.html (HTML)
- **Score**: ~80-90
- **Grade**: A or B
- **Errors**: None (has DOCTYPE, proper structure)
- **Recommendations**: Add meta tags, semantic HTML

### sample.java (Java)
- **Score**: ~75-80
- **Grade**: B or C
- **Errors**: Missing package declaration
- **Recommendations**: Add package, use logging framework

### sample.dart (Flutter)
- **Score**: ~70-80
- **Grade**: B or C
- **Errors**: Minimal
- **Recommendations**: Use const constructors, simplify build

## 🐛 Common Issues & Solutions

### Issue 1: "ModuleNotFoundError"
**Solution**: Install missing dependencies
```bash
pip install -r requirements.txt
```

### Issue 2: "Port already in use"
**Backend Solution**: 
```bash
# Find process using port 8000
lsof -i :8000
# Kill it
kill -9 <PID>
```

**Frontend Solution**:
```bash
# Streamlit will auto-select next available port
# Or specify port:
streamlit run app.py --server.port 8502
```

### Issue 3: Frontend can't connect to backend
**Solution**: 
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check `frontend/app.py` has correct API_URL
3. Disable firewall temporarily for testing

### Issue 4: File upload fails
**Solution**:
1. Check file extension is supported
2. Ensure file is text-based (not binary)
3. Try with provided sample files first

### Issue 5: Analysis returns mock results with API key
**Solution**:
1. Verify .env file is in `backend/` directory
2. Check API key is valid
3. Install optional dependencies:
   ```bash
   pip install openai anthropic
   ```

## 🎯 Quick Test Checklist

- [ ] Backend starts without errors
- [ ] `/health` endpoint returns success
- [ ] Frontend opens in browser
- [ ] Sidebar shows "API Connected"
- [ ] Can upload sample.py
- [ ] Analysis completes and shows results
- [ ] Score and grade display correctly
- [ ] Errors section shows (if any)
- [ ] Recommendations section shows
- [ ] Can test multiple files

## 🔄 Restart Services

### Restart Backend
```bash
# Press Ctrl+C to stop
# Then start again:
python main.py
```

### Restart Frontend
```bash
# Press Ctrl+C to stop
# Then start again:
streamlit run app.py
```

## 📝 Next Steps

Once everything is working:

1. **Test with your own code** - Upload your projects
2. **Compare results** - Try different code qualities
3. **Learn from feedback** - Read recommendations carefully
4. **Iterate and improve** - Fix errors and re-analyze
5. **Explore features** - Check "How It Works" tab

## 🎓 Understanding the Results

**Score Breakdown**:
- **Base Score**: 70 points (working code)
- **Bonuses**: Comments (+10), good structure (+5), proper length (+5)
- **Penalties**: Errors (-3 per error), bad practices (-5)

**Grade Scale**:
- A: 90-100 (Production-ready)
- B: 80-89 (Good quality)
- C: 70-79 (Acceptable)
- D: 60-69 (Needs work)
- F: 0-59 (Major issues)

## ✅ You're All Set!

Your AI Tutor Platform is now fully operational. Happy coding and learning! 🚀