from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from repositories.history_repository import HistoryRepository

router = APIRouter(
    prefix="/history",
    tags=["History"]
)


@router.get("/")
def get_history(
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return HistoryRepository.get_all(
        db=db,
        limit=limit
    )


@router.get("/{node_id}")
def get_node_history(
    node_id: str,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return HistoryRepository.get_by_node(
        db=db,
        node_id=node_id,
        limit=limit
    )