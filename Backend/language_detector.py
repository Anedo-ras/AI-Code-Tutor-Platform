import re
from typing import Optional


def detect_language(filename: str, code: str) -> str:
    """
    Detect programming language from filename and code content
    
    Args:
        filename: Name of the file
        code: Content of the file
        
    Returns:
        Detected language name
    """
    
    # Extension-based detection (primary method)
    extension = filename.split('.')[-1].lower() if '.' in filename else ''
    
    extension_map = {
        'py': 'python',
        'js': 'javascript',
        'jsx': 'javascript',
        'ts': 'typescript',
        'tsx': 'typescript',
        'java': 'java',
        'dart': 'dart',
        'html': 'html',
        'htm': 'html',
        'css': 'css',
        'scss': 'scss',
        'cs': 'csharp',
        'cpp': 'cpp',
        'c': 'c',
        'php': 'php',
        'rb': 'ruby',
        'go': 'go',
        'rs': 'rust',
        'swift': 'swift',
        'kt': 'kotlin',
        'sql': 'sql',
        'sh': 'shell',
        'bash': 'shell',
        'json': 'json',
        'xml': 'xml',
        'yaml': 'yaml',
        'yml': 'yaml'
    }
    
    if extension in extension_map:
        return extension_map[extension]
    
    # Content-based detection (fallback)
    return detect_language_from_content(code)


def detect_language_from_content(code: str) -> str:
    """
    Detect language from code content using pattern matching
    
    Args:
        code: Source code content
        
    Returns:
        Detected language name
    """
    
    code_lower = code.lower()
    
    # Python patterns
    if re.search(r'def\s+\w+\s*\(|import\s+\w+|from\s+\w+\s+import', code):
        return 'python'
    
    # JavaScript/TypeScript patterns
    if re.search(r'function\s+\w+|const\s+\w+\s*=|let\s+\w+\s*=|var\s+\w+', code):
        if 'interface' in code_lower or ': string' in code or ': number' in code:
            return 'typescript'
        return 'javascript'
    
    # Java patterns
    if re.search(r'public\s+class\s+\w+|private\s+\w+|import\s+java\.', code):
        return 'java'
    
    # C# patterns
    if re.search(r'using\s+System|namespace\s+\w+|public\s+class\s+\w+.*\{', code):
        if 'using System' in code or 'namespace' in code:
            return 'csharp'
    
    # Dart/Flutter patterns
    if re.search(r'import\s+[\'"]package:flutter|void\s+main\s*\(\)', code):
        return 'dart'
    
    # HTML patterns
    if re.search(r'<!DOCTYPE\s+html|<html|<head>|<body>', code_lower):
        return 'html'
    
    # CSS patterns
    if re.search(r'\{[^}]*:\s*[^;]+;|^\s*\.\w+\s*\{|^\s*#\w+\s*\{', code, re.MULTILINE):
        return 'css'
    
    # PHP patterns
    if '<?php' in code_lower or re.search(r'\$\w+\s*=', code):
        return 'php'
    
    # Ruby patterns
    if re.search(r'def\s+\w+|require\s+[\'"]|class\s+\w+\s*<', code):
        if 'require' in code or 'puts' in code:
            return 'ruby'
    
    # Go patterns
    if re.search(r'package\s+main|func\s+\w+|import\s+\(', code):
        return 'go'
    
    # SQL patterns
    if re.search(r'SELECT\s+.*FROM|CREATE\s+TABLE|INSERT\s+INTO', code_lower):
        return 'sql'
    
    # Default
    return 'unknown'


def get_language_info(language: str) -> dict:
    """
    Get additional information about a programming language
    
    Args:
        language: Language name
        
    Returns:
        Dictionary with language information
    """
    
    info_map = {
        'python': {
            'name': 'Python',
            'type': 'interpreted',
            'paradigm': 'multi-paradigm',
            'extensions': ['.py']
        },
        'javascript': {
            'name': 'JavaScript',
            'type': 'interpreted',
            'paradigm': 'multi-paradigm',
            'extensions': ['.js', '.jsx']
        },
        'typescript': {
            'name': 'TypeScript',
            'type': 'compiled to JavaScript',
            'paradigm': 'multi-paradigm',
            'extensions': ['.ts', '.tsx']
        },
        'java': {
            'name': 'Java',
            'type': 'compiled',
            'paradigm': 'object-oriented',
            'extensions': ['.java']
        },
        'dart': {
            'name': 'Dart',
            'type': 'compiled',
            'paradigm': 'object-oriented',
            'extensions': ['.dart']
        },
        'csharp': {
            'name': 'C#',
            'type': 'compiled',
            'paradigm': 'object-oriented',
            'extensions': ['.cs']
        },
        'html': {
            'name': 'HTML',
            'type': 'markup',
            'paradigm': 'declarative',
            'extensions': ['.html', '.htm']
        },
        'css': {
            'name': 'CSS',
            'type': 'stylesheet',
            'paradigm': 'declarative',
            'extensions': ['.css']
        }
    }
    
    return info_map.get(language, {
        'name': language.title(),
        'type': 'unknown',
        'paradigm': 'unknown',
        'extensions': []
    })