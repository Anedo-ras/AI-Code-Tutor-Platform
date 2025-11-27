import streamlit as st
import requests
import json
from typing import Optional

# Page configuration
st.set_page_config(
    page_title="AI Code Tutor Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .score-display {
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .grade-a { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
    .grade-b { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }
    .grade-c { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; }
    .grade-d { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; }
    .grade-f { background: linear-gradient(135deg, #30cfd0 0%, #330867 100%); color: white; }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1E88E5;
        margin: 1rem 0;
    }
    .error-card {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
    }
    .recommendation-card {
        background: #d1ecf1;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #17a2b8;
        margin: 0.5rem 0;
    }
    .strength-card {
        background: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_URL = "http://localhost:8000"


def check_api_health() -> bool:
    """Check if backend API is available"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def analyze_code(file) -> Optional[dict]:
    """Send code to backend for analysis"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(
            f"{API_URL}/analyze-code",
            files=files,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Analysis failed: {response.text}")
            return None
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to backend. Please ensure the API is running.")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


def main():
    # Header
    st.markdown('<div class="main-header">🎓 AI Code Tutor Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Upload your code and get instant AI-powered feedback</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📚 About")
        st.write("""
        This AI-powered platform analyzes your code and provides:
        - 🔍 Error detection
        - 💡 Recommendations
        - ⭐ Quality scoring
        - 📈 Improvement suggestions
        """)
        
        st.header("🔧 Supported Languages")
        languages = [
            "Python", "JavaScript", "TypeScript",
            "Java", "Dart/Flutter", "C#",
            "HTML", "CSS", "PHP", "Ruby",
            "Go", "Rust", "Swift", "Kotlin"
        ]
        for lang in languages:
            st.write(f"• {lang}")
        
        st.divider()
        
        # API Status
        api_status = check_api_health()
        if api_status:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Disconnected")
            st.info("Please start the backend server:\n```bash\ncd backend\npython main.py\n```")
    
    # Main content
    tab1, tab2 = st.tabs(["📤 Upload & Analyze", "📖 How It Works"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📁 Upload Your Code")
            
            uploaded_file = st.file_uploader(
                "Choose a code file",
                type=['py', 'js', 'jsx', 'ts', 'tsx', 'java', 'dart', 'html', 'css', 'cs', 'php', 'rb', 'go', 'rs', 'swift', 'kt'],
                help="Upload any supported code file for analysis"
            )
            
            if uploaded_file:
                st.success(f"✅ File loaded: {uploaded_file.name}")
                
                # Display code preview
                st.subheader("👀 Code Preview")
                code_content = uploaded_file.getvalue().decode('utf-8')
                st.code(code_content, language='python', line_numbers=True)
                
                # Analyze button
                if st.button("🚀 Analyze Code", type="primary", use_container_width=True):
                    with st.spinner("🔄 Analyzing your code..."):
                        # Reset file pointer
                        uploaded_file.seek(0)
                        result = analyze_code(uploaded_file)
                        
                        if result:
                            st.session_state['analysis_result'] = result
                            st.rerun()
        
        with col2:
            st.subheader("📊 Analysis Results")
            
            if 'analysis_result' in st.session_state:
                result = st.session_state['analysis_result']
                
                # Score display
                score = result['score']
                grade = result['grade']
                grade_class = f"grade-{grade.lower()}"
                
                st.markdown(
                    f'<div class="score-display {grade_class}">'
                    f'{score}/100<br><span style="font-size: 2rem;">Grade: {grade}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                
                # Language detection
                st.markdown(
                    f'<div class="metric-card">'
                    f'<strong>🔤 Detected Language:</strong> {result["language"].title()}'
                    f'</div>',
                    unsafe_allow_html=True
                )
                
                # Summary
                st.markdown(
                    f'<div class="metric-card">'
                    f'<strong>📝 Summary:</strong><br>{result["analysis_summary"]}'
                    f'</div>',
                    unsafe_allow_html=True
                )
                
                # Errors
                if result['errors']:
                    st.subheader("⚠️ Errors Found")
                    for error in result['errors']:
                        st.markdown(
                            f'<div class="error-card">'
                            f'<strong>Line {error.get("line", "N/A")}:</strong> {error.get("message", "Unknown error")}'
                            f'<br><small>Type: {error.get("type", "general")}</small>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.success("✅ No errors detected!")
                
                # Strengths
                if result.get('strengths'):
                    st.subheader("💪 Strengths")
                    for strength in result['strengths']:
                        st.markdown(
                            f'<div class="strength-card">✓ {strength}</div>',
                            unsafe_allow_html=True
                        )
                
                # Recommendations
                if result['recommendations']:
                    st.subheader("💡 Recommendations")
                    for i, rec in enumerate(result['recommendations'], 1):
                        st.markdown(
                            f'<div class="recommendation-card">{i}. {rec}</div>',
                            unsafe_allow_html=True
                        )
                
                # Download report button
                if st.button("📥 Download Report", use_container_width=True):
                    report = generate_report(result)
                    st.download_button(
                        label="💾 Save Report as JSON",
                        data=report,
                        file_name=f"code_analysis_report.json",
                        mime="application/json"
                    )
            else:
                st.info("👆 Upload a file and click 'Analyze Code' to see results")
    
    with tab2:
        st.subheader("🎯 How It Works")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 1️⃣ Upload
            Upload your code file in any supported programming language.
            """)
        
        with col2:
            st.markdown("""
            ### 2️⃣ Analyze
            Our AI engine performs:
            - Static analysis
            - Error detection
            - Best practice checks
            """)
        
        with col3:
            st.markdown("""
            ### 3️⃣ Learn
            Get actionable feedback:
            - Error explanations
            - Improvement tips
            - Quality score
            """)
        
        st.divider()
        
        st.subheader("🌟 Features")
        
        features = {
            "Multi-Language Support": "Supports 10+ programming languages",
            "Real-Time Analysis": "Get instant feedback on your code",
            "AI-Powered": "Uses advanced AI for intelligent recommendations",
            "Scoring System": "Clear grading from A to F",
            "Educational": "Learn best practices and improve skills",
            "Free to Use": "No registration required"
        }
        
        for feature, description in features.items():
            st.markdown(f"**{feature}:** {description}")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666;">
        Built with ❤️ using FastAPI and Streamlit | AI Code Tutor Platform v1.0
    </div>
    """, unsafe_allow_html=True)


def generate_report(result: dict) -> str:
    """Generate downloadable report"""
    report = {
        "analysis_report": result,
        "timestamp": st.session_state.get('timestamp', 'N/A')
    }
    return json.dumps(report, indent=2)


if __name__ == "__main__":
    main()