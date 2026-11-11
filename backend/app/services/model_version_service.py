from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.monitored_model import MonitoredModel
from app.models.model_version import ModelVersion
from app.schemas.model_version import ModelVersionCreate

def register_model_version(
    db: Session,
    version_data: ModelVersionCreate
):
    # Check whether the parent model exists
    parent_model = db.get(
        MonitoredModel,
        version_data.model_id
    )

    if parent_model is None:
        return None

    # Convert validated schema data into a database object
    new_version = ModelVersion(
        **version_data.model_dump()
    )

    try:
        db.add(new_version)
        db.commit()
        db.refresh(new_version)

        return new_version

    except IntegrityError:
        db.rollback()
        raise