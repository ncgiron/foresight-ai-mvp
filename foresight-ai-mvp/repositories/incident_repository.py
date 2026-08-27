from app.models import Incident


class IncidentRepository:

    def __init__(self, db):
        self.db = db

    def list(self):
        return self.db.query(Incident).all()

    def create(self, incident):
        self.db.add(incident)
        self.db.commit()
        self.db.refresh(incident)
        return incident