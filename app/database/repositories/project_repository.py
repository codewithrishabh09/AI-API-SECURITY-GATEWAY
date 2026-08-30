from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import ProjectCreate
import logging

logger = logging.getLogger(__name__)

class ProjectRepository:
    """Repository for Project model"""
    
    @staticmethod
    def create(db: Session, project_data: ProjectCreate, owner_id: int) -> Project:
        """Create new project"""
        db_project = Project(
            name=project_data.name,
            description=project_data.description,
            owner_id=owner_id
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        logger.info(f"Project created: {db_project.name} (Owner: {owner_id})")
        return db_project
    
    @staticmethod
    def get_by_id(db: Session, project_id: int) -> Project:
        """Get project by ID"""
        return db.query(Project).filter(Project.id == project_id).first()
    
    @staticmethod
    def get_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
        """Get projects by owner"""
        return db.query(Project).filter(
            Project.owner_id == owner_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, project_id: int, update_data: dict) -> Project:
        """Update project"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            for key, value in update_data.items():
                setattr(project, key, value)
            db.commit()
            db.refresh(project)
            logger.info(f"Project updated: {project.name}")
        return project
    
    @staticmethod
    def delete(db: Session, project_id: int) -> bool:
        """Delete project"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            db.delete(project)
            db.commit()
            logger.info(f"Project deleted: {project.name}")
            return True
        return False