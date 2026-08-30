from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    OWNER = "owner"
    MEMBER = "member"
    VIEWER = "viewer"

class APIKeyStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"

class ProjectStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class SecurityEventType(str, Enum):
    PROMPT_INJECTION = "prompt_injection"
    JAILBREAK_ATTEMPT = "jailbreak_attempt"
    PII_DETECTED = "pii_detected"
    SECRET_DETECTED = "secret_detected"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    POLICY_VIOLATION = "policy_violation"

class RequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    BLOCKED = "blocked"
    FAILED = "failed"

class PolicyType(str, Enum):
    RATE_LIMITING = "rate_limiting"
    COST_CONTROL = "cost_control"
    SECURITY_RULES = "security_rules"
    DATA_RETENTION = "data_retention"
    ACCESS_CONTROL = "access_control"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Constants
MAX_API_KEY_LENGTH = 64
API_KEY_PREFIX = "sk_"
MIN_PASSWORD_LENGTH = 8
MAX_POLICY_NAME_LENGTH = 255
MAX_PROJECT_NAME_LENGTH = 255