from fastapi import APIRouter

router = APIRouter(
    prefix="/api/incidents",
    tags=["Incidents"]
)


@router.get("")
def get_incidents():
    return {
        "message": "Incident API working"
    }