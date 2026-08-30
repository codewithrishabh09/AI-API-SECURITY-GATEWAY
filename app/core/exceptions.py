from fastapi import HTTPException, status

class SecurityGatewayException(Exception):
    """Base exception for security gateway"""
    pass

class AuthenticationException(SecurityGatewayException):
    """Raised when authentication fails"""
    def __init__(self, detail: str = "Authentication failed"):
        self.detail = detail
        super().__init__(self.detail)

class AuthorizationException(SecurityGatewayException):
    """Raised when authorization fails"""
    def __init__(self, detail: str = "Insufficient permissions"):
        self.detail = detail
        super().__init__(self.detail)

class InvalidAPIKeyException(SecurityGatewayException):
    """Raised when API key is invalid"""
    def __init__(self, detail: str = "Invalid API key"):
        self.detail = detail
        super().__init__(self.detail)

class RateLimitExceededException(SecurityGatewayException):
    """Raised when rate limit is exceeded"""
    def __init__(self, detail: str = "Rate limit exceeded"):
        self.detail = detail
        super().__init__(self.detail)

class SecurityViolationException(SecurityGatewayException):
    """Raised when security violation is detected"""
    def __init__(self, detail: str = "Security violation detected", violation_type: str = "unknown"):
        self.detail = detail
        self.violation_type = violation_type
        super().__init__(self.detail)

class PromptInjectionDetectedException(SecurityViolationException):
    """Raised when prompt injection is detected"""
    def __init__(self, detail: str = "Prompt injection detected"):
        super().__init__(detail, "prompt_injection")

class JailbreakDetectedException(SecurityViolationException):
    """Raised when jailbreak attempt is detected"""
    def __init__(self, detail: str = "Jailbreak attempt detected"):
        super().__init__(detail, "jailbreak")

class PIIDetectedException(SecurityViolationException):
    """Raised when PII is detected"""
    def __init__(self, detail: str = "PII detected in request"):
        super().__init__(detail, "pii_detected")

class InvalidPolicyException(SecurityGatewayException):
    """Raised when policy validation fails"""
    pass

class ProjectNotFoundException(SecurityGatewayException):
    """Raised when project is not found"""
    pass

class APIKeyNotFoundException(SecurityGatewayException):
    """Raised when API key is not found"""
    pass

# HTTP Exception Handlers
def get_http_exception(exc: SecurityGatewayException) -> HTTPException:
    """Convert SecurityGatewayException to HTTPException"""
    if isinstance(exc, AuthenticationException):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.detail
        )
    elif isinstance(exc, AuthorizationException):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.detail
        )
    elif isinstance(exc, RateLimitExceededException):
        return HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=exc.detail
        )
    elif isinstance(exc, (PromptInjectionDetectedException, JailbreakDetectedException, PIIDetectedException)):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.detail
        )
    else:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )