from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ConnectionBase(BaseModel):
    starting_board_id: int
    ending_board_id: int

class ConnectionCreate(ConnectionBase):
    pass

class ConnectionUpdate(ConnectionBase):
    pass
class ConnectionRead(ConnectionBase):
    connection_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
class ConnectionPatch(BaseModel):
    starting_board_id: Optional[int] = None
    ending_board_id: Optional[int] = None