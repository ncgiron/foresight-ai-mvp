from sqlalchemy.orm import Session

from app.models import KPIHistory


class HistoryRepository:

    @staticmethod
    def save(db: Session, record: KPIHistory):

        db.add(record)
        db.commit()
        db.refresh(record)

        return record

    @staticmethod
    def get_all(
        db: Session,
        limit: int = 100
    ):

        return (
            db.query(KPIHistory)
            .order_by(KPIHistory.timestamp.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_node(
        db: Session,
        node_id: str,
        limit: int = 100
    ):
        return (
            db.query(KPIHistory)
            .filter(KPIHistory.node_id == node_id)
            .order_by(KPIHistory.timestamp.desc())
            .limit(limit)
            .all()
        )