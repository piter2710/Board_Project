from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.connections import Connections

from database import Base


class Board(Base):
    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String)

    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now()
    )

    outgoing_connections: Mapped[list["Connections"]] = relationship(
        "Connections",
        foreign_keys="[Connections.starting_board_id]",
        back_populates="starting_board",
        cascade="all, delete-orphan"
    )

    incoming_connections: Mapped[list["Connections"]] = relationship(
        "Connections",
        foreign_keys="[Connections.ending_board_id]",
        back_populates="ending_board",
        cascade="all, delete-orphan"
    )