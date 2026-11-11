
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.schemas.monitored_model import (
    MonitoredModelCreate,
    MonitoredModelUpdate,
    MonitoredModelResponse
    
)

from app.services.model_service import (
    register_model,
    get_all_models,
    get_model_by_id,
    update_model,
    delete_model
)


router = APIRouter(
    prefix="/models",
    tags=["Models"]
)


# Create a new model
@router.post(
    "/",
    response_model=MonitoredModelResponse,
    status_code=status.HTTP_201_CREATED
)
def create_model(
    model_data: MonitoredModelCreate,
    db: Session = Depends(get_db)
):
    try:
        registered_model = register_model(db, model_data)
        return registered_model

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A model with this name already exists."
        )


# Retrieve all registered models
@router.get(
    "/",
    response_model=list[MonitoredModelResponse]
)

@router.get(
    "/{model_id}",
    response_model=MonitoredModelResponse
)
def retrieve_model(
    model_id: int,
    db: Session = Depends(get_db)
):
    model = get_model_by_id(db, model_id)

    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found."
        )

    return model
def list_models(
    db: Session = Depends(get_db)
):
    return get_all_models(db)

# Update an existing model
@router.patch(
    "/{model_id}",
    response_model=MonitoredModelResponse,
    summary="Update Model"
)
def modify_model(
    model_id: int,
    model_data: MonitoredModelUpdate,
    db: Session = Depends(get_db)
):
    try:
        model = update_model(db, model_id, model_data)

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A model with this name already exists."
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error)
        )

    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found."
        )

    return model


# Delete an existing model
@router.delete(
    "/{model_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Model"
)
def remove_model(
    model_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_model(db, model_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found."
        )

    return None
