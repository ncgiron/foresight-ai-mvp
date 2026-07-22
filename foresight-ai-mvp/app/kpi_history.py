from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime

from app.core.database import Base


class KPIHistory(Base):
    __tablename__ = "kpi_history"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(DateTime, index=True)

    node_id = Column(String, index=True)
    node_type = Column(String)

    cpu = Column(Float)

    sessions = Column(Integer)

    latency = Column(Float)

    throughput = Column(Float)

    packet_loss = Column(Float)

    availability = Column(Float)