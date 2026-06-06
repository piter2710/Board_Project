from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import database_connection
from models.connections import Connections
from schemas.connections import ConnectionCreate, ConnectionRead
from sqlalchemy import select
from typing import List
router = APIRouter(
    prefix="/connections",
    tags=["Connections"]
)

@router.get("/{connection_id}", response_model=ConnectionRead)
async def read_connection(connection_id: int, db: database_connection):
    stmt = select(Connections).where(Connections.connection_id == connection_id)
    result = await db.execute(stmt)
    connection = result.scalar_one_or_none()
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    return connection
@router.get("/", response_model=List[ConnectionRead])
async def read_connections(db: database_connection):
    stmt = select(Connections)
    result = await db.execute(stmt)
    connections = result.scalars().all()
    return connections
@router.post("/", response_model=ConnectionRead)
async def create_connection(connection: ConnectionCreate, db: database_connection):
    db_connection = Connections(**connection.model_dump())
    db.add(db_connection)
    await db.commit()
    await db.refresh(db_connection)
    return db_connection

@router.delete("/{connection_id}", response_model=ConnectionRead)
async def delete_connection(connection_id: int, db: database_connection):
    stmt = select(Connections).where(Connections.connection_id == connection_id)
    result = await db.execute(stmt)
    connection = result.scalar_one_or_none()
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    await db.delete(connection)
    await db.commit()
    return connection