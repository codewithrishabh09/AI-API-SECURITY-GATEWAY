from sqlalchemy.orm import Session
from app.security.pii_detector import PIIDetector
from app.security.secret_detector import SecretDetector
from app.security.prompt_injection import PromptInjectionDetector
from app.security.jailbreak_detector import JailbreakDetector
from app.security.moderation import ModerationService
from app.security.risk_engine import RiskEngine
from app.schemas.gateway import SecurityCheckResult
import logging

logger = logging.getLogger(__name__)

class SecurityService:
    
    pii_detector = PIIDetector()
    secret_detector = SecretDetector()
    prompt_injection_detector = PromptInjectionDetector()
    jailbreak_detector = JailbreakDetector()
    moderation_service = ModerationService()
    risk_engine = RiskEngine()
    
    @staticmethod
    def run_security_checks(
        db: Session,
        data: dict,
        project_id: int
    ) -> SecurityCheckResult:
        """Run all security checks"""
        violations = []
        risk_scores = {}
        
        # Convert data to string for analysis
        data_str = str(data)
        
        # Check for PII
        if PIIDetector.detect(data_str):
            violations.append("PII detected")
            risk_scores["pii"] = 0.9
        
        # Check for secrets
        if SecretDetector.detect(data_str):
            violations.append("Secret credentials detected")
            risk_scores["secrets"] = 0.95
        
        # Check for prompt injection
        if PromptInjectionDetector.detect(data_str):
            violations.append("Prompt injection attempt detected")
            risk_scores["prompt_injection"] = 0.85
        
        # Check for jailbreak attempts
        if JailbreakDetector.detect(data_str):
            violations.append("Jailbreak attempt detected")
            risk_scores["jailbreak"] = 0.8
        
        # Moderation check
        if ModerationService.check_content(data_str).is_flagged:
            violations.append("Content flagged by moderation")
            risk_scores["moderation"] = 0.7
        
        # Calculate overall risk
        max_risk = max(risk_scores.values()) if risk_scores else 0.0
        
        return SecurityCheckResult(
            is_safe=len(violations) == 0,
            violations=violations,
            risk_level="high" if max_risk > 0.7 else "medium" if max_risk > 0.3 else "low",
            details={"risk_scores": risk_scores}
        )