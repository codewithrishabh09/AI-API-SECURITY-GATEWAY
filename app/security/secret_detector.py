import re
from app.security.base import SecurityDetector

class SecretDetector(SecurityDetector):
    """Detect secrets and credentials"""
    
    # Patterns for secrets
    PATTERNS = {
        'api_key': r'(?i)(api[_-]?key|apikey)[=:\s]+[\'\"]*[a-zA-Z0-9\-_]{32,}[\'\"]*',
        'aws_key': r'AKIA[0-9A-Z]{16}',
        'github_token': r'ghp_[0-9a-zA-Z]{36}',
        'private_key': r'-----BEGIN (?:RSA|DSA|EC|OPENSSH|PRIVATE) KEY-----',
        'password': r'(?i)(password|passwd)[=:\s]+[\'\"]*[^\s\'\"]{8,}[\'\"]*',
        'database_url': r'(?i)(postgresql|mysql|mongodb)://[^\s]+'
    }
    
    @staticmethod
    def detect(text: str) -> bool:
        """Detect if text contains secrets"""
        for pattern_name, pattern in SecretDetector.PATTERNS.items():
            if re.search(pattern, text):
                return True
        return False
    
    @staticmethod
    def find_secrets(text: str) -> dict:
        """Find all secrets in text"""
        results = {}
        for pattern_name, pattern in SecretDetector.PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                results[pattern_name] = matches
        return results