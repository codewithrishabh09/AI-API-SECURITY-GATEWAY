import re
from app.security.base import SecurityDetector

class PIIDetector(SecurityDetector):
    """Detect Personally Identifiable Information"""
    
    # Patterns for PII
    PATTERNS = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b',
        'ssn': r'\b(?!000|666|9)\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b',
        'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
        'date_of_birth': r'\b(?:0?[1-9]|1[0-2])[/-](?:0?[1-9]|[12]\d|3[01])[/-](?:19|20)?\d{2}\b'
    }
    
    @staticmethod
    def detect(text: str) -> bool:
        """Detect if text contains PII"""
        for pattern_name, pattern in PIIDetector.PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    @staticmethod
    def find_pii(text: str) -> dict:
        """Find all PII in text"""
        results = {}
        for pattern_name, pattern in PIIDetector.PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                results[pattern_name] = matches
        return results