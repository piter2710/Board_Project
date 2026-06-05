
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class BoardBase(BaseModel):
    name: str
    description: Optional[str] = None
    
class BoardCreate(BoardBase):
    pass

class BoardUpdate(BoardBase):
    pass

class BoardRead(BoardBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)