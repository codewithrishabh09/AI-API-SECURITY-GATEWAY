from pydantic import BaseModel

class ContentModerationResult(BaseModel):
    is_flagged: bool
    categories: dict
    score: float

class ModerationService:
    """Content moderation service"""
    
    # Offensive words/phrases (example)
    BLOCKED_TERMS = [
        'hate', 'violence', 'abuse', 'explicit'
    ]
    
    @staticmethod
    def check_content(text: str) -> ContentModerationResult:
        """Check content for policy violations"""
        text_lower = text.lower()
        
        flagged = False
        for term in ModerationService.BLOCKED_TERMS:
            if term in text_lower:
                flagged = True
                break
        
        return ContentModerationResult(
            is_flagged=flagged,
            categories={'violence': 0, 'hate': 0, 'sexual': 0},
            score=0.5 if flagged else 0.1
        )