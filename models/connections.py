
from sqlalchemy import Integer, DateTime, func, ForeignKey
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.boards import Board

from database import Base


class Connections(Base):
    __tablename__ = "connections"
    
    connection_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    starting_board_id: Mapped[int] = mapped_column(Integer, ForeignKey("boards.id"), index=True)
    ending_board_id: Mapped[int] = mapped_column(Integer, ForeignKey("boards.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), onupdate=func.now())
    
    #Relationships
    starting_board: Mapped["Board"] = relationship(
        "Board", 
        foreign_keys=[starting_board_id], 
        back_populates="outgoing_connections"
    )
    ending_board: Mapped["Board"] = relationship(
        "Board", 
        foreign_keys=[ending_board_id], 
        back_populates="incoming_connections"
    )