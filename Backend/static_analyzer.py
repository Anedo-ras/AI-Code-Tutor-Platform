import re
from typing import Dict, List


class StaticAnalyzer:
    """Static code analyzer for multiple languages"""
    
    def analyze(self, code: str, language: str) -> Dict:
        """
        Perform static analysis on code
        
        Args:
            code: Source code to analyze
            language: Programming language
            
        Returns:
            Dictionary with errors and recommendations
        """
        
        analyzer_method = getattr(self, f'_analyze_{language}', self._analyze_generic)
        return analyzer_method(code)
    
    def _analyze_python(self, code: str) -> Dict:
        """Analyze Python code"""
        errors = []
        recommendations = []
        
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for syntax issues
            if line.strip().endswith('\\'):
                errors.append({
                    "type": "syntax",
                    "message": "Unnecessary line continuation",
                    "line": str(i)
                })
            
            # Check for common issues
            if re.search(r'except\s*:', line):
                errors.append({
                    "type": "best_practice",
                    "message": "Bare except clause - specify exception type",
                    "line": str(i)
                })
            
            if 'import *' in line:
                errors.append({
                    "type": "style",
                    "message": "Avoid wildcard imports",
                    "line": str(i)
                })
            
            # Check line length
            if len(line) > 120:
                recommendations.append(f"Line {i} exceeds 120 characters")
        
        # Check for missing docstrings
        if 'def ' in code and '"""' not in code and "'''" not in code:
            recommendations.append("Add docstrings to functions")
        
        # Check for proper spacing
        if re.search(r'\w+\(', code) and not re.search(r'\w+\s*\(', code):
            recommendations.append("Add spaces around operators for readability")
        
        return {
            "errors": errors,
            "recommendations": recommendations
        }
    
    def _analyze_javascript(self, code: str) -> Dict:
        """Analyze JavaScript code"""
        errors = []
        recommendations = []
        
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for var usage
            if re.search(r'\bvar\s+\w+', line):
                errors.append({
                    "type": "style",
                    "message": "Use 'const' or 'let' instead of 'var'",
                    "line": str(i)
                })
            
            # Check for == instead of ===
            if '==' in line and '===' not in line and '!=' in line and '!==' not in line:
                errors.append({
                    "type": "best_practice",
                    "message": "Use strict equality (===) instead of ==",
                    "line": str(i)
                })
            
            # Check for console.log (should be removed in production)
            if 'console.log' in line:
                recommendations.append(f"Line {i}: Remove console.log in production code")
        
        # Check for missing semicolons (basic check)
        if code.count(';') < len([l for l in lines if l.strip() and not l.strip().startswith('//')]): recommendations.append("Consider using semicolons consistently")
        
        # Check for function declarations
        if 'function' in code:
            recommendations.append("Consider using arrow functions for conciseness")
        
        return {
            "errors": errors,
            "recommendations": recommendations
        }
    
    def _analyze_java(self, code: str) -> Dict:
        """Analyze Java code"""
        errors = []
        recommendations = []
        
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for proper class naming
            if re.search(r'class\s+[a-z]', line):
                errors.append({
                    "type": "naming",
                    "message": "Class names should start with uppercase",
                    "line": str(i)
                })
            
            # Check for System.out.println
            if 'System.out.println' in line:
                recommendations.append(f"Line {i}: Use logging framework instead of System.out")
        
        # Check for main method
        if 'public static void main' in code:
            recommendations.append("Ensure proper exception handling in main method")
        
        # Check for package declaration
        if 'public class' in code and 'package ' not in code:
            recommendations.append("Add package declaration")
        
        return {
            "errors": errors,
            "recommendations": recommendations
        }
    
    def _analyze_dart(self, code: str) -> Dict:
        """Analyze Dart/Flutter code"""
        errors = []
        recommendations = []
        
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for proper widget structure
            if 'StatelessWidget' in line or 'StatefulWidget' in line:
                recommendations.append("Ensure widget follows Flutter best practices")
        
        # Check for build method
        if 'Widget build' in code:
            recommendations.append("Keep build method simple and extract complex widgets")
        
        # Check for const constructors
        if 'Widget' in code and 'const' not in code:
            recommendations.append("Use const constructors where possible for better performance")
        
        return {
            "errors": errors,
            "recommendations": recommendations
        }
    
    def _analyze_html(self, code: str) -> Dict:
        """Analyze HTML code"""
        errors = []
        recommendations = []
        
        code_lower = code.lower()
        
        # Check DOCTYPE
        if '<!doctype html>' not in code_lower:
            errors.append({
                "type": "structure",
                "message": "Missing DOCTYPE declaration",
                "line": "1"
            })
        
        # Check for html, head, body tags
        if '<html' not in code_lower:
            errors.append({
                "type": "structure",
                "message": "Missing <html> tag",
                "line": "N/A"
            })
        
        if '<head' not in code_lower:
            recommendations.append("Add <head> section with meta tags")
        
        if '<title>' not in code_lower:
            recommendations.append("Add <title> tag for SEO")
        
        # Check for alt attributes on images
        if '<img' in code_lower and 'alt=' not in code_lower:
            recommendations.append("Add alt attributes to images for accessibility")
        
        # Check for semantic HTML
        if '<div' in code_lower and not any(tag in code_lower for tag in ['<header', '<nav', '<main', '<footer']):
            recommendations.append("Use semantic HTML5 elements (header, nav, main, footer)")
        
        return {
            "errors": errors,
            "recommendations": recommendations
        }
    
    def _analyze_css(self, code: str) -> Dict:
        """Analyze CSS code"""
        errors = []
        recommendations = []
        
        lines = code.split('\n')
        
        # Check for !important
        if '!important' in code:
            recommendations.append("Avoid using !important - improve specificity instead")
        
        # Check for inline styles (if CSS contains style attributes)
        if 'style=' in code:
            recommendations.append("Move inline styles to CSS classes")
        
        # Check for vendor prefixes
        prefixes = ['-webkit-', '-moz-', '-ms-', '-o-']
        has_prefixes = any(prefix in code for prefix in prefixes)
        if has_prefixes:
            recommendations.append("Consider using autoprefixer instead of manual vendor prefixes")
        
        # Check for units on zero values
        if re.search(r':\s*0(px|em|rem|%)', code):
            recommendations.append("Remove units from zero values")
        
        return {
            "errors": errors,
            "recommendations": recommendations
        }
    
    def _analyze_csharp(self, code: str) -> Dict:
        """Analyze C# code"""
        errors = []
        recommendations = []
        
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for proper naming
            if re.search(r'class\s+[a-z]', line):
                errors.append({
                    "type": "naming",
                    "message": "Class names should use PascalCase",
                    "line": str(i)
                })
        
        # Check for using statements
        if 'using System' not in code:
            recommendations.append("Add necessary using statements")
        
        # Check for namespace
        if 'namespace' not in code and 'class' in code:
            recommendations.append("Organize code in namespaces")
        
        return {
            "errors": errors,
            "recommendations": recommendations
        }
    
    def _analyze_generic(self, code: str) -> Dict:
        """Generic analysis for unsupported languages"""
        recommendations = []
        
        lines = code.split('\n')
        num_lines = len(lines)
        
        # Basic recommendations
        if num_lines > 500:
            recommendations.append("Consider breaking large file into smaller modules")
        
        # Check for comments
        comment_lines = [l for l in lines if l.strip().startswith(('//','#','/*','*'))]
        if len(comment_lines) < num_lines * 0.1:
            recommendations.append("Add more comments to explain complex logic")
        
        return {
            "errors": [],
            "recommendations": recommendations
        }