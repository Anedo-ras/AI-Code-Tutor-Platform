Live Demo: Try the AI Tutor Platform here — an interactive code-analysis tool that evaluates your code, detects errors, and provides intelligent feedback in real time.
https://ai-code-tutor-platform.streamlit.app/

# 🎓 AI Tutor Platform - MVP

An AI-powered code analysis platform that helps developers learn and improve their code quality through intelligent feedback.

## 🌟 Features

- **Multi-Language Support**: Python, JavaScript, Java, Dart/Flutter, C#, HTML, CSS, and more
- **Real-Time Analysis**: Instant code evaluation and feedback
- **AI-Powered Insights**: Smart recommendations using LLM (mock or real)
- **Scoring System**: Clear grading from 0-100 with letter grades (A-F)
- **Error Detection**: Static analysis to catch common issues
- **Best Practices**: Learn industry-standard coding practices
- **User-Friendly Interface**: Clean Streamlit UI with modern design

## 🏗️ Architecture

```
Frontend (Streamlit) → Backend (FastAPI) → AI Engine (LLM/Mock)
```

## 📋 Prerequisites

- Python 3.8+
- pip package manager
- (Optional) OpenAI or Anthropic API key for real LLM analysis

## 🚀 Quick Start

### 1. Clone or Create Project Structure

```bash
mkdir ai_tutor_platform
cd ai_tutor_platform
```

Create the following structure:
```
ai_tutor_platform/
├── backend/
├── frontend/
└── test_samples/
```

### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies

```bash
cd ../frontend
pip install -r requirements.txt
```

### 4. (Optional) Configure API Keys

Create a `.env` file in the `backend/` directory:

```bash
# For OpenAI
OPENAI_API_KEY=your_openai_key_here

# OR for Anthropic Claude
ANTHROPIC_API_KEY=your_anthropic_key_here
```

**Note**: The platform works perfectly without API keys using mock responses!

### 5. Start the Backend

```bash
cd backend
python main.py
```

The API will start at `http://localhost:8000`

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 6. Start the Frontend (New Terminal)

```bash
cd frontend
streamlit run app.py
```

The UI will open at `http://localhost:8501`

## 📝 Usage

1. Open the Streamlit interface at `http://localhost:8501`
2. Click "Browse files" and upload a code file
3. Click "🚀 Analyze Code"
4. View your results:
   - Score out of 100
   - Letter grade (A-F)
   - Detected errors
   - Recommendations
   - Code strengths

## 🧪 Testing with Sample Files

Use the provided sample files in `test_samples/`:

- `sample.py` - Python code
- `sample.js` - JavaScript code
- `sample.html` - HTML page
- `sample.java` - Java code
- `sample.dart` - Flutter/Dart code

## 📊 API Endpoints

### Health Check
```bash
GET http://localhost:8000/health
```

### Analyze Code
```bash
POST http://localhost:8000/analyze-code
Content-Type: multipart/form-data
Body: file (code file)
```

Response:
```json
{
  "language": "python",
  "errors": [...],
  "recommendations": [...],
  "score": 85,
  "analysis_summary": "...",
  "strengths": [...],
  "grade": "B"
}
```

## 🛠️ Technology Stack

- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **AI Engine**: OpenAI/Anthropic (optional), Mock responses (default)
- **Static Analysis**: Custom analyzers for each language

## 🎯 Supported Languages

- Python (.py)
- JavaScript (.js, .jsx)
- TypeScript (.ts, .tsx)
- Java (.java)
- Dart/Flutter (.dart)
- C# (.cs)
- HTML (.html, .htm)
- CSS (.css)
- PHP (.php)
- Ruby (.rb)
- Go (.go)
- Rust (.rs)
- Swift (.swift)
- Kotlin (.kt)

## 🔧 Configuration

### Backend Port
Edit `backend/main.py`, line with `uvicorn.run()`:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change port here
```

### Frontend API URL
Edit `frontend/app.py`:
```python
API_URL = "http://localhost:8000"  # Change if backend is on different port
```

## 📈 Scoring System

- **90-100**: Grade A (Excellent)
- **80-89**: Grade B (Good)
- **70-79**: Grade C (Satisfactory)
- **60-69**: Grade D (Needs Improvement)
- **0-59**: Grade F (Poor)

## 🐛 Troubleshooting

### Backend won't start
- Check if port 8000 is already in use
- Verify all dependencies are installed: `pip install -r backend/requirements.txt`

### Frontend can't connect to backend
- Ensure backend is running first
- Check API URL in `frontend/app.py`
- Look for "✅ API Connected" in sidebar

### File upload fails
- Check file extension is supported
- Verify file is text-based (not binary)
- Check file size (keep under 1MB for best results)

## 🚢 Deployment

### Deploy Backend (Example with Docker)

Create `Dockerfile` in backend/:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### Deploy Frontend (Streamlit Cloud)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy!

## 📄 License

This is an MVP project for educational purposes.

## 🤝 Contributing

This is a learning platform MVP. Feel free to extend it with:
- More languages
- Better static analysis
- Real-time collaboration
- Code diff comparison
- Historical tracking

## 📞 Support

For issues or questions, refer to the documentation or check:
- FastAPI docs: https://fastapi.tiangolo.com
- Streamlit docs: https://docs.streamlit.io

---

**Built with ❤️ for developers learning to code better**
