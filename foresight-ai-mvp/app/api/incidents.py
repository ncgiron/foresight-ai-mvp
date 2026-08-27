from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from repositories.incident_repository import IncidentRepository
from services.incidents.similarity import find_similar_incidents

router = APIRouter(
    prefix="/api/incidents",
    tags=["Incidents"]
)

@router.get("")
def get_incidents(
    db: Session = Depends(get_db)
):
    repo = IncidentRepository(db)
    return repo.list()


@router.post("/search")
def search_incidents(
    query: str,
    db: Session = Depends(get_db)
):
    repo = IncidentRepository(db)

    incidents = repo.list()

    return find_similar_incidents(
        incidents,
        query
    )