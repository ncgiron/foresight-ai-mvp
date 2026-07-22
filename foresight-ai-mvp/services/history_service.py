from datetime import datetime

from app.models import KPIHistory
from repositories.history_repository import HistoryRepository


# class HistoryService:

#     @staticmethod
#     def store_kpi(db, node):

#         record = KPIHistory(
#             timestamp=datetime.utcnow(),

#             node_id=node["node"],
#             node_type=node["technology"],

#             cpu=node["cpu"],

#             sessions=node["active_sessions"],

#             latency=0.0,

#             throughput=node["throughput_gbps"],

#             packet_loss=node["packet_loss"],

#             availability=99.99
#         )

#         return HistoryRepository.save(db, record)

class HistoryService:

    @staticmethod
    def store_kpi(db, node):
        ...

    @staticmethod
    def get_history(
        db,
        limit: int = 100
    ):
        """
        Retrieve KPI history.

        Parameters
        ----------
        limit : int

        Returns
        -------
        list
        """

        return HistoryRepository.get_all(
            db=db,
            limit=limit
        )

    @staticmethod
    def get_node_history(
        db,
        node_id: str,
        limit: int = 100
    ):
        """
        Retrieve KPI history for a
        specific network function.

        Parameters
        ----------
        node_id : str

        limit : int

        Returns
        -------
        list
        """

        return HistoryRepository.get_by_node(
            db=db,
            node_id=node_id,
            limit=limit
        )