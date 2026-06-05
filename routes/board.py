from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import database_connection
from models.boards import Board
from schemas.boards import BoardRead, BoardCreate, BoardUpdate, BoardBase
from sqlalchemy import select
router = APIRouter(
    prefix="/boards",
    tags=["Boards"]
)

@router.post("/", response_model=BoardRead)
async def create_board(board: BoardCreate, db: database_connection):
    db_board = Board(**board.model_dump())
    db.add(db_board)
    await db.commit()
    await db.refresh(db_board)
    return db_board

@router.get("/{board_id}", response_model=BoardRead)
async def read_board(board_id: int, db: database_connection):
    result = await db.get(Board, board_id)
    if not result:
        raise HTTPException(status_code=404, detail="Board not found")
    return result
@router.get("/", response_model=list[BoardRead])
async def read_boards(db: database_connection, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Board).offset(skip).limit(limit))
    return result.scalars().all()
@router.put("/{board_id}", response_model=BoardRead)
async def update_board(board_id: int, board_update: BoardUpdate, db: database_connection):
    board = await db.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    for key, value in board_update.model_dump(exclude_unset=True).items():
        setattr(board, key, value)
    await db.commit()
    await db.refresh(board)
    return board

@router.patch("/{board_id}", response_model=BoardRead)
async def partial_update_board(board_id: int, board_update: BoardBase, db: database_connection):
    board = await db.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    for key, value in board_update.model_dump(exclude_unset=True).items():
        setattr(board, key, value)
    await db.commit()
    await db.refresh(board)
    return board

@router.delete("/{board_id}", response_model=BoardRead)
async def delete_board(board_id: int, db: database_connection):
    board = await db.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    await db.delete(board)
    await db.commit()
    return board

