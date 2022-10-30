import pymongo
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from dependency_injector.providers import Configuration
from src.classes.events.log import Log
from src.classes.events.metric import Metric
from src.classes.events.mission import Mission, Event

COLLECTIONS = {"log": "logging", "mission": "mission", "metric": "metric"}
MAPPING = {Log: "log", Mission: "mission", Metric: "metric"}


class DatabaseService:
    _config: Configuration
    _client: MongoClient
    _database: Database
    _collections: dict[str, Collection]

    def __init__(self, config: Configuration):
        self._config = config

    def connect(self):
        self._client = MongoClient(self._config["database"]["connection_string"])
        self._database = self._client[self._config["database"]["name"]]
        self._collections = {key: self._database[collection] for key, collection in COLLECTIONS.items()}

    def add(self, event: Event):
        self.add_many([event])

    def add_many(self, logs: list[Event]):
        if len(logs) == 0:
            return
        self._add_many(logs, MAPPING[logs[0].__class__])

    def get_logs(self, mission_id: str):
        cursor = self._collections["log"].find({"mission_id": mission_id}).sort("timestamp_ms", pymongo.DESCENDING)
        for log in cursor:
            yield Log(**DatabaseService._convert_from(log))

    def get_metrics(self, mission_id: str):
        cursor = self._collections["metric"].find({"mission_id": mission_id}).sort("timestamp_ms", pymongo.DESCENDING)
        for log in cursor:
            yield Metric(**DatabaseService._convert_from(log))

    def get_mission(self, id: str):
        return DatabaseService._convert_from(self._collections["mission"].find_one(id))

    def get_missions(self):
        cursor = self._collections["mission"].find({}).sort("end_time_ms", pymongo.DESCENDING)
        for mission in cursor:
            yield Mission(**DatabaseService._convert_from(mission))

    def _add_many(self, elems: list, collection_name: str):
        dict_elems = [elem.to_dict() for elem in elems]
        self._collections[collection_name].insert_many(dict_elems)

    @staticmethod
    def _convert_from(event):
        if event.get("_id"):
            event["id"] = str(event.pop("_id"))
        return event
