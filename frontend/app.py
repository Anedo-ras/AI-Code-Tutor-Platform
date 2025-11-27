import streamlit as st
import requests
import json
from typing import Optional
from datetime import datetime
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas

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


def generate_pdf_report(result: dict, filename: str, code_preview: str = "") -> BytesIO:
    """Generate a beautiful PDF report"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1E88E5'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#666666'),
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=colors.HexColor('#444444'),
        spaceAfter=10,
        alignment=TA_JUSTIFY
    )
    
    # Title
    elements.append(Paragraph("🎓 AI Code Tutor Platform", title_style))
    elements.append(Paragraph("Code Analysis Report", styles['Heading2']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Report Info
    report_info = [
        ['Report Date:', datetime.now().strftime('%B %d, %Y at %I:%M %p')],
        ['File Name:', filename],
        ['Language:', result['language'].title()],
    ]
    
    info_table = Table(report_info, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Score Section - Eye-catching
    score = result['score']
    grade = result['grade']
    
    # Determine color based on grade
    grade_colors = {
        'A': colors.HexColor('#4CAF50'),
        'B': colors.HexColor('#2196F3'),
        'C': colors.HexColor('#FF9800'),
        'D': colors.HexColor('#FF5722'),
        'F': colors.HexColor('#F44336')
    }
    grade_color = grade_colors.get(grade, colors.grey)
    
    score_data = [
        ['SCORE', 'GRADE'],
        [f'{score}/100', grade]
    ]
    
    score_table = Table(score_data, colWidths=[3*inch, 3*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E88E5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, 1), 36),
        ('TEXTCOLOR', (0, 1), (-1, 1), grade_color),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ('TOPPADDING', (0, 0), (-1, -1), 20),
        ('GRID', (0, 0), (-1, -1), 2, colors.HexColor('#1E88E5')),
        ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#1E88E5')),
    ]))
    elements.append(score_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Summary Section
    elements.append(Paragraph("📝 Analysis Summary", heading_style))
    summary_text = result.get('analysis_summary', 'No summary available')
    elements.append(Paragraph(summary_text, body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Strengths Section
    if result.get('strengths'):
        elements.append(Paragraph("💪 Code Strengths", heading_style))
        
        strengths_data = [['#', 'Strength']]
        for i, strength in enumerate(result['strengths'], 1):
            strengths_data.append([str(i), strength])
        
        strengths_table = Table(strengths_data, colWidths=[0.5*inch, 5.5*inch])
        strengths_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f9f0')]),
        ]))
        elements.append(strengths_table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Errors Section
    if result.get('errors'):
        elements.append(Paragraph("⚠️ Errors & Issues", heading_style))
        
        errors_data = [['Line', 'Type', 'Message']]
        for error in result['errors']:
            errors_data.append([
                error.get('line', 'N/A'),
                error.get('type', 'general'),
                error.get('message', 'Unknown error')
            ])
        
        errors_table = Table(errors_data, colWidths=[0.7*inch, 1.3*inch, 4*inch])
        errors_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ffc107')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#333333')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fff9e6')]),
        ]))
        elements.append(errors_table)
        elements.append(Spacer(1, 0.2*inch))
    else:
        elements.append(Paragraph("⚠️ Errors & Issues", heading_style))
        elements.append(Paragraph("✅ No errors detected! Great job!", body_style))
        elements.append(Spacer(1, 0.2*inch))
    
    # Recommendations Section
    if result.get('recommendations'):
        elements.append(Paragraph("💡 Recommendations", heading_style))
        
        rec_data = [['#', 'Recommendation']]
        for i, rec in enumerate(result['recommendations'], 1):
            rec_data.append([str(i), rec])
        
        rec_table = Table(rec_data, colWidths=[0.5*inch, 5.5*inch])
        rec_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#17a2b8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#e9f7f9')]),
        ]))
        elements.append(rec_table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Footer
    elements.append(Spacer(1, 0.4*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Generated by AI Code Tutor Platform | Helping developers write better code", footer_style))
    elements.append(Paragraph(f"Report ID: {datetime.now().strftime('%Y%m%d%H%M%S')}", footer_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


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
                            st.session_state['filename'] = uploaded_file.name
                            st.session_state['code_content'] = code_content
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
                
                # Download report button - NOW GENERATES PDF
                st.divider()
                col_a, col_b = st.columns(2)
                
                with col_a:
                    if st.button("📥 Download PDF Report", use_container_width=True, type="primary"):
                        with st.spinner("📄 Generating beautiful PDF report..."):
                            pdf_buffer = generate_pdf_report(
                                result, 
                                st.session_state.get('filename', 'code_file'),
                                st.session_state.get('code_content', '')
                            )
                            
                            st.download_button(
                                label="💾 Save PDF Report",
                                data=pdf_buffer,
                                file_name=f"code_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                            st.success("✅ PDF Report generated successfully!")
                
                with col_b:
                    # Also offer JSON for developers who want raw data
                    json_report = json.dumps({
                        "analysis_report": result,
                        "filename": st.session_state.get('filename', 'code_file'),
                        "timestamp": datetime.now().isoformat()
                    }, indent=2)
                    
                    st.download_button(
                        label="📋 Download JSON (Dev)",
                        data=json_report,
                        file_name=f"code_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
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
            - Beautiful PDF report
            """)
        
        st.divider()
        
        st.subheader("🌟 Features")
        
        features = {
            "Multi-Language Support": "Supports 10+ programming languages",
            "Real-Time Analysis": "Get instant feedback on your code",
            "AI-Powered": "Uses advanced AI for intelligent recommendations",
            "Scoring System": "Clear grading from A to F",
            "Educational": "Learn best practices and improve skills",
            "PDF Reports": "Beautiful, professional PDF reports to save and share",
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


if __name__ == "__main__":
    main()