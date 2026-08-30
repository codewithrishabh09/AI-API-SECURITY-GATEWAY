from app.security.base import SecurityDetector

class JailbreakDetector(SecurityDetector):
    """Detect jailbreak attempts"""
    
    # Common jailbreak phrases
    JAILBREAK_PHRASES = [
        'pretend',
        'hypothetically',
        'roleplaying',
        'for research purposes',
        'educational purposes',
        'in a fictional scenario',
        'as a thought experiment',
        'without restrictions',
        'ignoring safety guidelines',
        'evil mode',
        'unrestricted',
        'no restrictions'
    ]
    
    @staticmethod
    def detect(text: str) -> bool:
        """Detect jailbreak attempts"""
        text_lower = text.lower()
        
        for phrase in JailbreakDetector.JAILBREAK_PHRASES:
            if phrase in text_lower:
                return True
        
        return False