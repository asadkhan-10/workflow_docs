# app/routers/workflows.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/workflows", tags=["Workflows"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.WorkflowOut
)
def create_workflow(
    workflow: schemas.WorkflowCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    new_workflow = models.Workflow(owner_id=current_user.id, **workflow.model_dump())
    db.add(new_workflow)
    db.commit()
    db.refresh(new_workflow)
    return new_workflow


@router.get("/", response_model=list[schemas.WorkflowOut])
def get_workflows(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    workflows = (
        db.query(models.Workflow)
        .filter(models.Workflow.owner_id == current_user.id)
        .all()
    )
    return workflows


@router.get("/{id}", response_model=schemas.WorkflowOut)
def get_workflow(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    workflow = (
        db.query(models.Workflow)
        .filter(models.Workflow.id == id, models.Workflow.owner_id == current_user.id)
        .first()
    )
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found"
        )
    return workflow


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workflow(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    workflow = (
        db.query(models.Workflow)
        .filter(models.Workflow.id == id, models.Workflow.owner_id == current_user.id)
        .first()
    )
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found"
        )
    db.delete(workflow)
    db.commit()
