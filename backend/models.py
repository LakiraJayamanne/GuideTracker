from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Position(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    latitude: float
    longitude: float
    state: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
