from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import List
from models.project import Project
from db.session import get_db

router = APIRouter(
    prefix="/project",
    tags=['PROJECTS']
)
# Schema Definitions
class ProjectBase(BaseModel):
    project_description: str
    user_id: int

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    created_date: datetime
    modified_date: datetime

    class Config:
        orm_mode = True

# CRUD Functions
def create_project(db: Session, project_data: ProjectCreate):
    db_project = Project(**project_data.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Project).offset(skip).limit(limit).all()

def update_project(db: Session, project_id: int, project_data: ProjectCreate):
    db_project = get_project(db, project_id)
    if db_project:
        for key, value in project_data.dict().items():
            setattr(db_project, key, value)
        db.commit()
        db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project

# API Endpoints
@router.post("/projects/", response_model=ProjectResponse)
def create_project_endpoint(project_data: ProjectCreate, db: Session = Depends(get_db)):
    return create_project(db=db, project_data=project_data)

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.get("/projects/", response_model=List[ProjectResponse])
def read_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    projects = get_projects(db, skip=skip, limit=limit)
    return projects

@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project_endpoint(project_id: int, project_data: ProjectCreate, db: Session = Depends(get_db)):
    db_project = update_project(db, project_id=project_id, project_data=project_data)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.delete("/projects/{project_id}", response_model=ProjectResponse)
def delete_project_endpoint(project_id: int, db: Session = Depends(get_db)):
    db_project = delete_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project
