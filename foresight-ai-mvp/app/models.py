from pydantic import BaseModel
from typing import Dict, List
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
from app.core.database import Base
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy import Numeric

from app.core.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String, primary_key=True)

    timestamp = Column(DateTime)

    node = Column(String(255))
    nf_type = Column(String(50))

    root_cause = Column(Text)
    diagnosis = Column(Text)

    recommendation = Column(Text)

    confidence = Column(Numeric(5, 2))

    confirmed = Column(Boolean)

    scenario = Column(String(255))

class NodeKPI(BaseModel):
    node: str
    cpu_usage: float
    memory_usage: float
    throughput_mbps: float
    sessions: int
    latency_ms: float


class NetworkState(BaseModel):
    timestamp: str
    nodes: Dict[str, NodeKPI]

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

