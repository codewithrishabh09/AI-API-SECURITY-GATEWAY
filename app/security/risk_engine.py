class RiskEngine:
    """Calculate risk scores for requests"""
    
    @staticmethod
    def calculate_risk_score(
        pii_detected: bool = False,
        secrets_detected: bool = False,
        injection_detected: bool = False,
        jailbreak_detected: bool = False,
        flagged_content: bool = False
    ) -> dict:
        """Calculate overall risk score"""
        risk_score = 0.0
        
        if pii_detected:
            risk_score += 0.2
        if secrets_detected:
            risk_score += 0.3
        if injection_detected:
            risk_score += 0.25
        if jailbreak_detected:
            risk_score += 0.15
        if flagged_content:
            risk_score += 0.1
        
        # Normalize to 0-1
        risk_score = min(risk_score, 1.0)
        
        # Determine risk level
        if risk_score >= 0.7:
            risk_level = "critical"
        elif risk_score >= 0.5:
            risk_level = "high"
        elif risk_score >= 0.3:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "score": round(risk_score, 2),
            "level": risk_level
        }