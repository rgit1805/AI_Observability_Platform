from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.monitored_model import MonitoredModel
from app.schemas.monitored_model import (
    MonitoredModelCreate,
    MonitoredModelUpdate
)
from sqlalchemy import select

def register_model(
    db: Session,
    model_data: MonitoredModelCreate
) -> MonitoredModel:

    model = MonitoredModel(
        **model_data.model_dump()
    )

    try:
        db.add(model)
        db.commit()
        db.refresh(model)

    except IntegrityError:
        db.rollback()
        raise

    return model

def get_all_models(db: Session) -> list[MonitoredModel]:

    statement = select(MonitoredModel).order_by(
        MonitoredModel.created_at.desc()
    )

    models = db.scalars(statement).all()

    return list(models)

def get_model_by_id(
    db: Session,
    model_id: int
) -> MonitoredModel | None:

    statement = select(MonitoredModel).where(
        MonitoredModel.id == model_id
    )

    model = db.scalar(statement)

    return model

def update_model(
    db: Session,
    model_id: int,
    model_data: MonitoredModelUpdate
) -> MonitoredModel | None:

    # Find the existing model
    model = db.get(MonitoredModel, model_id)

    if model is None:
        return None

    # Extract only fields the client actually provided
    update_data = model_data.model_dump(exclude_unset=True)

    # Prevent NULL values in database columns that cannot be NULL
    for field in ("name", "model_type", "provider"):
        if field in update_data and update_data[field] is None:
            raise ValueError(f"{field} cannot be null.")

    # Apply the changes
    for field, value in update_data.items():
        setattr(model, field, value)

    try:
        db.commit()
        db.refresh(model)

    except IntegrityError:
        db.rollback()
        raise

    return model

def delete_model(
    db: Session,
    model_id: int
) -> bool:

    # Find the model
    model = db.get(MonitoredModel, model_id)

    # Return False if it doesn't exist
    if model is None:
        return False

    # Delete the database record
    db.delete(model)

    # Permanently save the deletion
    db.commit()

    return True