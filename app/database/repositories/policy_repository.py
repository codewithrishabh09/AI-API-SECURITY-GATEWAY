from sqlalchemy.orm import Session
from app.models.policy import Policy
from app.schemas.policy import PolicyCreate
import logging

logger = logging.getLogger(__name__)

class PolicyRepository:
    """Repository for Policy model"""
    
    @staticmethod
    def create(db: Session, policy_data: PolicyCreate, project_id: int) -> Policy:
        """Create new policy"""
        db_policy = Policy(
            name=policy_data.name,
            description=policy_data.description,
            policy_type=policy_data.policy_type,
            rules=policy_data.rules,
            project_id=project_id
        )
        db.add(db_policy)
        db.commit()
        db.refresh(db_policy)
        logger.info(f"Policy created: {db_policy.name}")
        return db_policy
    
    @staticmethod
    def get_by_id(db: Session, policy_id: int) -> Policy:
        """Get policy by ID"""
        return db.query(Policy).filter(Policy.id == policy_id).first()
    
    @staticmethod
    def get_by_project(db: Session, project_id: int, skip: int = 0, limit: int = 100):
        """Get policies by project"""
        return db.query(Policy).filter(
            Policy.project_id == project_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, policy_id: int, update_data: dict) -> Policy:
        """Update policy"""
        policy = db.query(Policy).filter(Policy.id == policy_id).first()
        if policy:
            for key, value in update_data.items():
                setattr(policy, key, value)
            db.commit()
            db.refresh(policy)
            logger.info(f"Policy updated: {policy.name}")
        return policy
    
    @staticmethod
    def delete(db: Session, policy_id: int) -> bool:
        """Delete policy"""
        policy = db.query(Policy).filter(Policy.id == policy_id).first()
        if policy:
            db.delete(policy)
            db.commit()
            logger.info(f"Policy deleted: {policy.name}")
            return True
        return False