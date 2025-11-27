from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
from ai_engine import AICodeAnalyzer
from language_detector import detect_language
from static_analyzer import StaticAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Tutor Platform API",
    description="Code analysis and tutoring API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzers
ai_analyzer = AICodeAnalyzer()
static_analyzer = StaticAnalyzer()


class AnalysisResponse(BaseModel):
    language: str
    errors: List[Dict[str, str]]
    recommendations: List[str]
    score: int
    analysis_summary: str
    strengths: List[str]
    grade: str


@app.get("/")
async def root():
    return {
        "message": "AI Tutor Platform API",
        "version": "1.0.0",
        "endpoints": ["/health", "/analyze-code"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Tutor Platform",
        "ai_engine": "ready"
    }


@app.post("/analyze-code", response_model=AnalysisResponse)
async def analyze_code(file: UploadFile = File(...)):
    """
    Analyze uploaded code file
    
    - Detects programming language
    - Performs static analysis
    - Uses AI to evaluate code quality
    - Returns score, errors, and recommendations
    """
    try:
        # Read file content
        content = await file.read()
        code = content.decode('utf-8')
        
        logger.info(f"Analyzing file: {file.filename}")
        
        # Detect language
        language = detect_language(file.filename, code)
        logger.info(f"Detected language: {language}")
        
        # Perform static analysis
        static_results = static_analyzer.analyze(code, language)
        
        # AI-powered analysis
        ai_results = await ai_analyzer.analyze_code(
            code=code,
            language=language,
            filename=file.filename
        )
        
        # Merge results
        errors = static_results.get("errors", []) + ai_results.get("errors", [])
        recommendations = static_results.get("recommendations", []) + ai_results.get("recommendations", [])
        
        # Calculate final score
        score = calculate_score(errors, ai_results.get("score", 75))
        grade = get_grade(score)
        
        response = AnalysisResponse(
            language=language,
            errors=errors[:10],  # Limit to top 10 errors
            recommendations=recommendations[:8],  # Limit to top 8 recommendations
            score=score,
            analysis_summary=ai_results.get("summary", "Code analysis completed."),
            strengths=ai_results.get("strengths", [])[:5],
            grade=grade
        )
        
        logger.info(f"Analysis complete. Score: {score}/100")
        return response
        
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File encoding error. Please upload a valid text file."
        )
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


def calculate_score(errors: List[Dict], base_score: int) -> int:
    """Calculate final score based on errors and AI score"""
    error_penalty = len(errors) * 3
    final_score = max(0, min(100, base_score - error_penalty))
    return final_score


def get_grade(score: int) -> str:
    """Convert score to letter grade"""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)