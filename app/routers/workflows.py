# app/routers/workflows.py
from xxlimited import Str

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from app.ai import generate_workflow_documentation

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


@router.post("/{id}/generate-docs", status_code=status.HTTP_200_OK)
def generate_docs(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    # Fetch the workflow and verify ownership
    workflow = (
        db.query(models.Workflow)
        .filter(models.Workflow.id == id, models.Workflow.owner_id == current_user.id)
        .first()
    )

    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow with id {id} not found",
        )

    # Generate documentation using Gemini
    try:
        documentation = generate_workflow_documentation(
            title=str(workflow.title),
            raw_input=str(workflow.raw_input),
            input_type=str(workflow.input_type)
        )
         # Save generated docs back to DB
        workflow.documentation = documentation  # type: ignore
        db.commit()
        db.refresh(workflow)

        return {"documentation": documentation}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Documentation generation failed: {str(e)}"
        )

   

