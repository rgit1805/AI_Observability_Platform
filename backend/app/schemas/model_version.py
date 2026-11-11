from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Literal

class ModelVersionCreate(BaseModel):

    model_id: int = Field(gt=0)

    version: str = Field(
    min_length=5,
    max_length=30,
    pattern=r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$"
)

   

    artifact_uri: str | None = None

    description: str | None = None

class ModelVersionUpdate(BaseModel):

    artifact_uri: str | None = Field(
        default=None,
        max_length=500
    )

    description: str | None = None

    status: Literal[
        "registered",
        "active",
        "archived"
    ] | None = None

class ModelVersionResponse(BaseModel):

    id: int
    model_id: int
    version: str
    artifact_uri: str | None
    description: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)