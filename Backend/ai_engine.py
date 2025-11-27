import os
import json
from typing import Dict, List
import logging
import re

logger = logging.getLogger(__name__)


class AICodeAnalyzer:
    """AI-powered code analyzer with mock and real LLM support"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        self.use_real_llm = bool(self.api_key)
        
        if self.use_real_llm:
            logger.info("AI Engine: Using real LLM")
        else:
            logger.info("AI Engine: Using mock responses")
    
    async def analyze_code(self, code: str, language: str, filename: str) -> Dict:
        """Main analysis method"""
        if self.use_real_llm:
            return await self._analyze_with_llm(code, language, filename)
        else:
            return self._mock_analysis(code, language, filename)
    
    async def _analyze_with_llm(self, code: str, language: str, filename: str) -> Dict:
        """Real LLM analysis using OpenAI or Claude"""
        try:
            if os.getenv("OPENAI_API_KEY"):
                return await self._openai_analysis(code, language)
            elif os.getenv("ANTHROPIC_API_KEY"):
                return await self._claude_analysis(code, language)
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            return self._mock_analysis(code, language, filename)
    
    async def _openai_analysis(self, code: str, language: str) -> Dict:
        """OpenAI GPT analysis"""
        try:
            import openai
            openai.api_key = os.getenv("OPENAI_API_KEY")
            
            prompt = self._create_analysis_prompt(code, language)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer and tutor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content
            return self._parse_llm_response(result)
            
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return self._mock_analysis(code, language, "file")
    
    async def _claude_analysis(self, code: str, language: str) -> Dict:
        """Claude API analysis"""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            prompt = self._create_analysis_prompt(code, language)
            
            message = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            result = message.content[0].text
            return self._parse_llm_response(result)
            
        except Exception as e:
            logger.error(f"Claude error: {e}")
            return self._mock_analysis(code, language, "file")
    
    def _create_analysis_prompt(self, code: str, language: str) -> str:
        """Create analysis prompt for LLM"""
        return f"""Analyze this {language} code and provide:

1. Errors or issues (if any)
2. Code quality score (0-100)
3. Recommendations for improvement
4. Strengths of the code
5. Summary

Code:
```{language}
{code}
```

Respond in JSON format:
{{
    "errors": [list of error descriptions],
    "score": integer from 0-100,
    "recommendations": [list of recommendations],
    "strengths": [list of strengths],
    "summary": "brief summary"
}}"""
    
    def _parse_llm_response(self, response: str) -> Dict:
        """Parse LLM response into structured format"""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback parsing
                return {
                    "errors": [],
                    "score": 75,
                    "recommendations": [response[:200]],
                    "strengths": ["Code is readable"],
                    "summary": response[:150]
                }
        except Exception as e:
            logger.error(f"Parse error: {e}")
            return self._default_response()
    
    def _mock_analysis(self, code: str, language: str, filename: str) -> Dict:
        """Mock analysis when no API key is available"""
        
        # Simple heuristics
        lines = code.split('\n')
        num_lines = len(lines)
        has_comments = any('#' in line or '//' in line or '/*' in line for line in lines)
        avg_line_length = sum(len(line) for line in lines) / max(num_lines, 1)
        
        # Calculate base score
        score = 70
        
        if has_comments:
            score += 10
        if num_lines > 20:
            score += 5
        if avg_line_length < 100:
            score += 5
        
        errors = []
        recommendations = []
        strengths = []
        
        # Language-specific mock analysis
        if language == "python":
            if "import *" in code:
                errors.append({
                    "type": "style",
                    "message": "Avoid wildcard imports (import *)",
                    "line": "multiple"
                })
                score -= 5
            
            if not has_comments:
                recommendations.append("Add docstrings to functions and classes")
            
            if "def " in code:
                strengths.append("Uses functions for code organization")
            
            recommendations.extend([
                "Consider using type hints for better code clarity",
                "Follow PEP 8 style guidelines",
                "Add error handling with try-except blocks"
            ])
        
        elif language == "javascript":
            if "var " in code:
                errors.append({
                    "type": "style",
                    "message": "Use 'const' or 'let' instead of 'var'",
                    "line": "multiple"
                })
                score -= 5
            
            if "function" in code:
                strengths.append("Uses functions for modularity")
            
            recommendations.extend([
                "Use ES6+ features like arrow functions and destructuring",
                "Add JSDoc comments for better documentation",
                "Consider using async/await for asynchronous operations"
            ])
        
        elif language == "java":
            if "public class" in code:
                strengths.append("Follows object-oriented principles")
            
            recommendations.extend([
                "Ensure proper exception handling",
                "Use meaningful variable names",
                "Follow Java naming conventions"
            ])
        
        elif language == "html":
            if "<!DOCTYPE html>" not in code:
                errors.append({
                    "type": "structure",
                    "message": "Missing DOCTYPE declaration",
                    "line": "1"
                })
                score -= 5
            
            if "<title>" in code:
                strengths.append("Includes page title")
            
            recommendations.extend([
                "Add meta tags for better SEO",
                "Use semantic HTML5 elements",
                "Ensure accessibility with ARIA labels"
            ])
        
        elif language == "css":
            strengths.append("Styles are organized")
            recommendations.extend([
                "Use CSS variables for maintainability",
                "Consider using a preprocessor like SASS",
                "Organize styles with BEM methodology"
            ])
        
        # Generic recommendations
        if num_lines < 10:
            recommendations.append("Consider breaking code into smaller, reusable functions")
        
        if not has_comments:
            score -= 5
            recommendations.append("Add comments to explain complex logic")
        
        summary = f"This {language} code shows {'good' if score >= 75 else 'moderate'} quality. "
        summary += f"The file contains {num_lines} lines of code. "
        
        if errors:
            summary += f"Found {len(errors)} issue(s) that should be addressed. "
        else:
            summary += "No major issues detected. "
        
        summary += "Review the recommendations for further improvements."
        
        return {
            "errors": errors,
            "score": min(100, max(0, score)),
            "recommendations": recommendations[:8],
            "strengths": strengths if strengths else ["Code structure is clear"],
            "summary": summary
        }
    
    def _default_response(self) -> Dict:
        """Default response structure"""
        return {
            "errors": [],
            "score": 75,
            "recommendations": ["Review code structure and organization"],
            "strengths": ["Code is functional"],
            "summary": "Analysis completed with default scoring."
        }