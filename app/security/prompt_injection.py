import re
from app.security.base import SecurityDetector

class PromptInjectionDetector(SecurityDetector):
    """Detect prompt injection attacks"""
    
    # Keywords that indicate prompt injection
    INJECTION_KEYWORDS = [
        'ignore previous',
        'ignore the system',
        'bypass',
        'override',
        'forget',
        'system prompt',
        'instructions',
        'do not follow',
        'instead of'
    ]
    
    # SQL injection patterns
    SQL_PATTERNS = [
        r"('\s*OR\s*'|'\s*;|DROP|INSERT|UPDATE|DELETE|UNION|SELECT)",
        r"--\s*$",
        r"/\*.*\*/",
        r"xp_cmdshell"
    ]
    
    @staticmethod
    def detect(text: str) -> bool:
        """Detect prompt injection"""
        text_lower = text.lower()
        
        # Check for injection keywords
        for keyword in PromptInjectionDetector.INJECTION_KEYWORDS:
            if keyword in text_lower:
                return True
        
        # Check for SQL patterns
        for pattern in PromptInjectionDetector.SQL_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False