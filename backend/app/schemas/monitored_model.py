from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MonitoredModelCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)

    model_type: Literal["traditional_ml", "llm"]

    provider: str = Field(min_length=1, max_length=50)

    description: str | None = None


class MonitoredModelResponse(BaseModel):
    id: int
    name: str
    model_type: str
    provider: str
    description: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MonitoredModelUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150
    )

    model_type: Literal[
        "traditional_ml",
        "llm"
    ] | None = None

    provider: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    description: str | None = None